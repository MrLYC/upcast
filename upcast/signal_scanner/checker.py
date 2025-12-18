"""AST visitor for detecting signal patterns."""

from typing import Any

from astroid import MANAGER, nodes

from upcast.signal_scanner.signal_parser import (
    categorize_celery_signal,
    categorize_django_signal,
    parse_celery_connect_decorator,
    parse_custom_signal_definition,
    parse_receiver_decorator,
    parse_signal_connect_method,
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
        self.signals: dict[str, dict[str, dict[str, list[dict[str, Any]]]]] = {
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

        # Second pass: collect signal handlers
        self._collect_signal_handlers(module)

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

        # Initialize signal list if needed
        if signal_name not in self.signals[framework][category]:
            self.signals[framework][category][signal_name] = []

        # Add handler
        self.signals[framework][category][signal_name].append(handler)

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
                    has_handlers = True

                if not has_handlers:
                    unused.append(signal_def)

            if unused and self.verbose:
                if "django" not in results:
                    results["django"] = {}
                results["django"]["unused_custom_signals"] = unused

        return results

    def get_summary(self) -> dict[str, Any]:
        """Get summary statistics.

        Returns:
            Summary dictionary with counts
        """
        summary: dict[str, Any] = {}

        # Django counts
        django_count = 0
        for _category_name, category in self.signals["django"].items():
            # Skip non-dict categories (like unused_custom_signals which is a list)
            if not isinstance(category, dict):
                continue
            for handlers in category.values():
                django_count += len(handlers)

        if django_count > 0:
            summary["django_handlers"] = django_count

        # Celery counts
        celery_count = 0
        for _category_name, category in self.signals["celery"].items():
            # Skip non-dict categories
            if not isinstance(category, dict):
                continue
            for handlers in category.values():
                celery_count += len(handlers)

        if celery_count > 0:
            summary["celery_handlers"] = celery_count

        # Custom signals
        if self.custom_signals:
            summary["custom_signals_defined"] = len(self.custom_signals)

        return summary
