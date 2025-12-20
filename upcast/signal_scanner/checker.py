"""AST visitor for detecting signal patterns."""

from typing import Any

from astroid import MANAGER, nodes

from upcast.signal_scanner.signal_parser import (
    SignalUsage,
    categorize_celery_signal,
    categorize_django_signal,
    parse_celery_connect_decorator,
    parse_custom_signal_definition,
    parse_receiver_decorator,
    parse_signal_connect_method,
    parse_signal_send,
)


class SignalChecker:
    """AST visitor that detects Django and Celery signal patterns."""

    def __init__(self, root_path: str | None = None, verbose: bool = False):
        """Initialize the checker.

        Args:
            root_path: Root path for calculating module names
            verbose: Enable verbose output
        """
        self.root_path = root_path
        self.verbose = verbose

        # Signal collections grouped by framework and type
        # New structure: {receivers: [], senders: [], usages: []}
        self.signals: dict[str, dict[str, dict[str, dict[str, list]]]] = {
            "django": {},
            "celery": {},
        }

        # Custom signal definitions (Django)
        self.custom_signals: dict[str, dict[str, Any]] = {}

        # Import tracking for signal name resolution
        self.django_imports: set[str] = set()
        self.celery_imports: set[str] = set()

    def visit_module(self, module: nodes.Module) -> None:
        """Visit a module and extract signal patterns.

        Args:
            module: The astroid Module node to visit
        """
        # First pass: collect import information and custom signal definitions
        self._collect_imports(module)
        self._collect_custom_signals(module)

        # Second pass: collect signal handlers (receivers)
        self._collect_signal_handlers(module)

        # Third pass: collect signal sends
        self._collect_signal_sends(module)

    def _collect_imports(self, module: nodes.Module) -> None:
        """Collect signal imports for resolution.

        Args:
            module: The module to scan
        """
        for import_node in module.nodes_of_class(nodes.ImportFrom):
            if not import_node.modname:
                continue

            # Track Django signal imports
            if "django" in import_node.modname and "signal" in import_node.modname:
                for name, _ in import_node.names:
                    self.django_imports.add(name)

            # Track Celery signal imports
            elif "celery" in import_node.modname and "signal" in import_node.modname:
                for name, _ in import_node.names:
                    self.celery_imports.add(name)

            # Track django.dispatch imports
            elif import_node.modname == "django.dispatch":
                for name, _ in import_node.names:
                    if name == "receiver" or name == "Signal":
                        self.django_imports.add(name)

    def _collect_custom_signals(self, module: nodes.Module) -> None:
        """Collect custom Signal() definitions.

        Args:
            module: The module to scan
        """
        for assign_node in module.nodes_of_class(nodes.Assign):
            signal_def = parse_custom_signal_definition(assign_node, self.root_path)
            if signal_def:
                signal_name = signal_def["name"]
                self.custom_signals[signal_name] = signal_def

    def _collect_signal_handlers(self, module: nodes.Module) -> None:
        """Collect signal handler registrations.

        Args:
            module: The module to scan
        """
        # Collect decorator-based handlers
        for func_node in module.nodes_of_class(nodes.FunctionDef):
            # Django @receiver decorator
            django_handlers = parse_receiver_decorator(func_node, self.root_path)
            for handler in django_handlers:
                self._register_handler("django", handler)

            # Celery @signal.connect decorator
            celery_handlers = parse_celery_connect_decorator(func_node, self.root_path)
            for handler in celery_handlers:
                self._register_handler("celery", handler)

        # Collect .connect() method calls
        for call_node in module.nodes_of_class(nodes.Call):
            handler = parse_signal_connect_method(call_node, self.root_path)
            if handler:
                # Determine framework based on imports
                signal_name = handler["signal"]
                if signal_name in self.django_imports or signal_name in self.custom_signals:
                    self._register_handler("django", handler)
                elif signal_name in self.celery_imports:
                    self._register_handler("celery", handler)
                else:
                    # Try to categorize by known signal names
                    if categorize_django_signal(signal_name) != "other_signals":
                        self._register_handler("django", handler)
                    elif categorize_celery_signal(signal_name) != "other_signals":
                        self._register_handler("celery", handler)

    def _collect_signal_sends(self, module: nodes.Module) -> None:
        """Collect signal.send() and signal.send_robust() calls.

        Args:
            module: The module to scan
        """
        # Get known signal names from receivers for whitelist validation
        known_signal_names = self._get_known_signal_names()

        file_path = module.file or "<unknown>"

        # Scan all Call nodes for signal sends
        for call_node in module.nodes_of_class(nodes.Call):
            result = parse_signal_send(
                call_node,
                self.django_imports,
                self.celery_imports,
                self.custom_signals,
                known_signal_names,
                self.root_path,
                file_path,
            )
            if result:
                signal_name, usage = result
                # Determine framework
                if signal_name in self.django_imports or signal_name in self.custom_signals:
                    self._register_send("django", signal_name, usage)
                elif signal_name in self.celery_imports:
                    self._register_send("celery", signal_name, usage)
                else:
                    # Try to categorize
                    if categorize_django_signal(signal_name) != "other_signals":
                        self._register_send("django", signal_name, usage)
                    elif categorize_celery_signal(signal_name) != "other_signals":
                        self._register_send("celery", signal_name, usage)

    def _get_known_signal_names(self) -> set[str]:
        """Extract all signal names that have receivers.

        Returns:
            Set of signal names
        """
        known = set()
        for framework_signals in self.signals.values():
            for category_signals in framework_signals.values():
                known.update(category_signals.keys())
        return known

    def _register_handler(self, framework: str, handler: dict[str, Any]) -> None:
        """Register a signal handler in the appropriate category.

        Args:
            framework: 'django' or 'celery'
            handler: Handler dictionary with signal, handler, file, line
        """
        signal_name = handler["signal"]

        # Determine category
        if framework == "django":
            # Check if it's a custom signal
            if signal_name in self.custom_signals:  # noqa: SIM108
                category = "custom_signals"
            else:
                category = categorize_django_signal(signal_name)
        else:  # celery
            category = categorize_celery_signal(signal_name)

        # Initialize category if needed
        if category not in self.signals[framework]:
            self.signals[framework][category] = {}

        # Initialize signal structure if needed
        if signal_name not in self.signals[framework][category]:
            self.signals[framework][category][signal_name] = {
                "receivers": [],
                "senders": [],
                "usages": [],
            }

        # Add to receivers
        self.signals[framework][category][signal_name]["receivers"].append(handler)

        # Create usage from handler
        usage = self._handler_to_usage(handler)
        self.signals[framework][category][signal_name]["usages"].append(usage)

    def _register_send(self, framework: str, signal_name: str, usage: SignalUsage) -> None:
        """Register a signal send call.

        Args:
            framework: 'django' or 'celery'
            signal_name: Name of the signal
            usage: SignalUsage object
        """
        # Determine category
        if framework == "django":
            if signal_name in self.custom_signals:  # noqa: SIM108
                category = "custom_signals"
            else:
                category = categorize_django_signal(signal_name)
        else:  # celery
            category = categorize_celery_signal(signal_name)

        # Initialize category if needed
        if category not in self.signals[framework]:
            self.signals[framework][category] = {}

        # Initialize signal structure if needed
        if signal_name not in self.signals[framework][category]:
            self.signals[framework][category][signal_name] = {
                "receivers": [],
                "senders": [],
                "usages": [],
            }

        # Convert usage to sender dict for backward compatibility
        sender_dict = {
            "file": usage.file,
            "line": usage.line,
            "pattern": usage.pattern,
        }
        if usage.sender:
            sender_dict["sender"] = usage.sender

        # Add to senders and usages
        self.signals[framework][category][signal_name]["senders"].append(sender_dict)
        self.signals[framework][category][signal_name]["usages"].append(usage)

    def _handler_to_usage(self, handler: dict[str, Any]) -> SignalUsage:
        """Convert handler dict to SignalUsage object.

        Args:
            handler: Handler dictionary

        Returns:
            SignalUsage object
        """
        return SignalUsage(
            file=handler.get("file", "<unknown>"),
            line=handler.get("line", 0),
            column=handler.get("column", 0),
            pattern=handler.get("pattern", "unknown"),
            code=handler.get("code", ""),
            sender=handler.get("sender"),
        )

    def check_file(self, file_path: str) -> None:
        """Parse and visit a Python file to detect signal patterns.

        Args:
            file_path: Absolute path to the Python file
        """
        try:
            # Parse the file with astroid
            module = MANAGER.ast_from_file(file_path)
            # Visit the AST
            self.visit_module(module)
        except Exception as e:
            # Log error but continue with other files
            if self.verbose:
                print(f"Error parsing {file_path}: {e!s}")

    def get_results(self) -> dict[str, Any]:
        """Get collected signal patterns.

        Returns:
            Dictionary with django and celery signal groups
        """
        results: dict[str, Any] = {}

        # Add Django signals
        if self.signals["django"]:
            results["django"] = self.signals["django"]

        # Add Celery signals
        if self.signals["celery"]:
            results["celery"] = self.signals["celery"]

        # Add custom signal definitions if any are unused
        if self.custom_signals:
            unused = []
            for signal_name, signal_def in self.custom_signals.items():
                # Check if signal has handlers
                has_handlers = False
                if (
                    "custom_signals" in self.signals["django"]
                    and signal_name in self.signals["django"]["custom_signals"]
                ):
                    sig_data = self.signals["django"]["custom_signals"][signal_name]
                    # Check if it has receivers or senders
                    has_handlers = bool(sig_data.get("receivers") or sig_data.get("senders"))

                if not has_handlers:
                    unused.append(signal_def)

            if unused and self.verbose:
                if "django" not in results:
                    results["django"] = {}
                results["django"]["unused_custom_signals"] = unused

        return results

    def get_summary(self) -> dict[str, Any]:  # noqa: C901
        """Get summary statistics.

        Returns:
            Summary dictionary with counts
        """
        summary: dict[str, Any] = {}

        # Django counts
        django_receivers = 0
        django_senders = 0
        for _category_name, category in self.signals["django"].items():
            # Skip non-dict categories (like unused_custom_signals which is a list)
            if not isinstance(category, dict):
                continue
            for signal_data in category.values():
                if isinstance(signal_data, dict):
                    django_receivers += len(signal_data.get("receivers", []))
                    django_senders += len(signal_data.get("senders", []))

        # Celery counts
        celery_receivers = 0
        celery_senders = 0
        for _category_name, category in self.signals["celery"].items():
            # Skip non-dict categories
            if not isinstance(category, dict):
                continue
            for signal_data in category.values():
                if isinstance(signal_data, dict):
                    celery_receivers += len(signal_data.get("receivers", []))
                    celery_senders += len(signal_data.get("senders", []))

        if django_receivers > 0 or django_senders > 0:
            summary["django_receivers"] = django_receivers
            if django_senders > 0:
                summary["django_senders"] = django_senders

        if celery_receivers > 0 or celery_senders > 0:
            summary["celery_receivers"] = celery_receivers
            if celery_senders > 0:
                summary["celery_senders"] = celery_senders

        # Custom signals
        if self.custom_signals:
            summary["custom_signals_defined"] = len(self.custom_signals)

        return summary
