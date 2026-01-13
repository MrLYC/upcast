"""Logging scanner for detecting logging patterns across Python projects.

Supports multiple logging libraries: logging, loguru, structlog, Django.
"""

import re
import time
from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.ast_utils import safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.logging import FileLoggingInfo, LogCall, LoggingOutput, LoggingSummary


class LoggingScanner(BaseScanner[LoggingOutput]):
    """Scanner for detecting logging patterns in Python code."""

    # Default sensitive keywords that might indicate logging of sensitive data
    DEFAULT_SENSITIVE_KEYWORDS: ClassVar[set[str]] = {
        "password",
        "passwd",
        "pwd",
        "token",
        "api_key",
        "apikey",
        "secret",
        "ssn",
        "social_security",
        "credit_card",
        "creditcard",
        "cvv",
        "private_key",
        "privatekey",
    }

    # Log level methods
    LOG_LEVELS: ClassVar[set[str]] = {"debug", "info", "warning", "warn", "error", "critical", "fatal", "exception"}

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
        check_sensitive: bool = True,
        sensitive_keywords: list[str] | None = None,
    ):
        """Initialize scanner.

        Args:
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose logging
            check_sensitive: Enable sensitive data detection
            sensitive_keywords: Custom sensitive keywords to detect (uses default if None)
        """
        super().__init__(include_patterns, exclude_patterns, verbose)
        self.check_sensitive = check_sensitive
        # Use custom keywords if provided, otherwise use defaults
        self.sensitive_keywords = set(sensitive_keywords) if sensitive_keywords else self.DEFAULT_SENSITIVE_KEYWORDS
        # Compile regex patterns for efficient matching
        # Pattern for message content matching (uses word boundaries)
        self._sensitive_pattern = re.compile(r"\b(" + "|".join(self.sensitive_keywords) + r")\b", re.IGNORECASE)
        # Pattern for JWT token detection
        self._jwt_pattern = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")
        # Pre-compile patterns for argument name matching (with underscore boundaries)
        # This avoids recompiling in the hot path during scanning
        self._arg_patterns = [
            re.compile(r"(?:^|_|\b)" + re.escape(keyword) + r"(?:$|_|\b)", re.IGNORECASE)
            for keyword in self.sensitive_keywords
        ]

    def scan(self, path: Path) -> LoggingOutput:
        """Scan path for logging patterns.

        Args:
            path: Directory or file path to scan

        Returns:
            Complete scan output with summary and results
        """
        start_time = time.time()
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent

        results: dict[str, FileLoggingInfo] = {}

        for file_path in files:
            file_info = self._scan_file(file_path, base_path)
            if file_info:
                rel_path = get_relative_path_str(file_path, base_path)
                results[rel_path] = file_info

        scan_duration_ms = int((time.time() - start_time) * 1000)
        summary = self._calculate_summary(results, scan_duration_ms)

        return LoggingOutput(
            summary=summary,
            results=results,
            metadata={"scanner_name": "logging"},
        )

    def _scan_file(self, file_path: Path, base_path: Path) -> FileLoggingInfo | None:
        """Scan a single file for logging patterns.

        Args:
            file_path: Path to Python file
            base_path: Base path for module resolution

        Returns:
            FileLoggingInfo if file contains logging, None otherwise
        """
        module = self.parse_file(file_path)
        if not module:
            return None

        # Resolve module path for logger name resolution
        module_path = self._get_module_path(file_path, base_path)

        # Track imports to detect which libraries are used
        imports = self._detect_imports(module)

        # Track loggers created in this file
        loggers: dict[str, str] = {}  # variable_name -> logger_name
        logger_types: dict[str, str] = {}  # variable_name -> library type

        # Collect log calls
        logging_calls: list[LogCall] = []
        loguru_calls: list[LogCall] = []
        structlog_calls: list[LogCall] = []
        django_calls: list[LogCall] = []

        # Phase 1: Detect logger creation
        self._detect_logger_creation(module, loggers, logger_types, module_path, imports)

        # Phase 2: Detect log method calls
        self._detect_log_calls(
            module,
            loggers,
            logger_types,
            module_path,
            imports,
            logging_calls,
            loguru_calls,
            structlog_calls,
            django_calls,
        )

        # Return None if no logging detected
        if not (logging_calls or loguru_calls or structlog_calls or django_calls):
            return None

        return FileLoggingInfo(
            logging=logging_calls,
            loguru=loguru_calls,
            structlog=structlog_calls,
            django=django_calls,
        )

    def _get_module_path(self, file_path: Path, base_path: Path) -> str:
        """Convert file path to Python module path.

        Args:
            file_path: Path to Python file
            base_path: Base path for resolution

        Returns:
            Module path like 'myapp.services.auth'
        """
        try:
            relative = file_path.resolve().relative_to(base_path.resolve())
            if relative.stem == "__init__":
                parts = list(relative.parts[:-1])
            else:
                parts = [*list(relative.parts[:-1]), relative.stem]
            return ".".join(parts) if parts else "root"
        except ValueError:
            return "root"

    def _detect_imports(self, module: nodes.Module) -> dict[str, str]:
        """Detect imported logging libraries.

        Args:
            module: Parsed AST module

        Returns:
            Mapping of import names to library types
        """
        imports: dict[str, str] = {}

        for node in module.nodes_of_class((nodes.Import, nodes.ImportFrom)):
            if isinstance(node, nodes.Import):
                self._process_import(node, imports)
            elif isinstance(node, nodes.ImportFrom):
                self._process_import_from(node, imports)

        return imports

    def _process_import(self, node: nodes.Import, imports: dict[str, str]) -> None:
        """Process regular import statements.

        Args:
            node: Import node
            imports: Dictionary to populate
        """
        for name, alias in node.names:
            import_name = alias if alias else name
            if name in {"logging", "loguru", "structlog"}:
                imports[import_name] = name

    def _process_import_from(self, node: nodes.ImportFrom, imports: dict[str, str]) -> None:
        """Process from...import statements.

        Args:
            node: ImportFrom node
            imports: Dictionary to populate
        """
        module_name = node.modname
        lib_type = None

        if module_name == "logging":
            lib_type = "logging"
        elif module_name == "loguru":
            lib_type = "loguru"
        elif module_name == "structlog":
            lib_type = "structlog"
        elif module_name and "django" in module_name and "logging" in module_name:
            lib_type = "django"

        if lib_type:
            for name, alias in node.names:
                import_name = alias if alias else name
                imports[import_name] = lib_type

    def _detect_logger_creation(
        self,
        module: nodes.Module,
        loggers: dict[str, str],
        logger_types: dict[str, str],
        module_path: str,
        imports: dict[str, str],
    ) -> None:
        """Detect logger creation and track variable assignments.

        Args:
            module: Parsed AST module
            loggers: Dictionary to populate with logger variables
            logger_types: Dictionary to populate with logger library types
            module_path: Module path for __name__ resolution
            imports: Detected imports mapping
        """
        for node in module.nodes_of_class(nodes.Assign):
            # Check if assignment is a logger creation
            if isinstance(node.value, nodes.Call):
                logger_name, lib_type = self._get_logger_name_from_call(node.value, module_path, imports)
                if logger_name and lib_type:
                    # Track all assigned variables
                    for target in node.targets:
                        if isinstance(target, nodes.AssignName):
                            loggers[target.name] = logger_name
                            logger_types[target.name] = lib_type

    def _get_logger_name_from_call(
        self, call: nodes.Call, module_path: str, imports: dict[str, str]
    ) -> tuple[str, str] | tuple[None, None]:
        """Extract logger name from getLogger() or similar call.

        Args:
            call: Call node
            module_path: Module path for __name__ resolution
            imports: Detected imports mapping

        Returns:
            Tuple of (logger_name, library_type) or (None, None)
        """
        func_name = safe_as_string(call.func)

        # Standard library: logging.getLogger()
        if "getLogger" in func_name:
            if call.args:
                arg = call.args[0]
                if isinstance(arg, nodes.Name) and arg.name == "__name__":
                    return (module_path, "logging")
                logger_name = infer_value(arg).get_if_type(str)
                return (logger_name if logger_name is not None else "root", "logging")
            return ("root", "logging")

        # Loguru: from loguru import logger
        # Loguru uses a pre-configured logger instance
        if isinstance(call.func, nodes.Name) and call.func.name in imports and imports[call.func.name] == "loguru":
            return ("loguru", "loguru")

        # Structlog: structlog.get_logger()
        if "get_logger" in func_name and "structlog" in func_name:
            if call.args:
                logger_name = infer_value(call.args[0]).get_if_type(str)
                return (logger_name if logger_name is not None else module_path, "structlog")
            return (module_path, "structlog")

        return (None, None)

    def _detect_log_calls(
        self,
        module: nodes.Module,
        loggers: dict[str, str],
        logger_types: dict[str, str],
        module_path: str,
        imports: dict[str, str],
        logging_calls: list[LogCall],
        loguru_calls: list[LogCall],
        structlog_calls: list[LogCall],
        django_calls: list[LogCall],
    ) -> None:
        """Detect all logging method calls in the module.

        Args:
            module: Parsed AST module
            loggers: Tracked logger variables
            logger_types: Tracked logger library types
            module_path: Module path for resolution
            imports: Detected imports mapping
            logging_calls: List to populate with stdlib logging calls
            loguru_calls: List to populate with loguru calls
            structlog_calls: List to populate with structlog calls
            django_calls: List to populate with Django calls
        """
        for node in module.nodes_of_class(nodes.Call):
            if not isinstance(node.func, nodes.Attribute):
                continue

            method_name = node.func.attrname
            if method_name not in self.LOG_LEVELS:
                continue

            # Determine logger variable, name, and library type
            logger_name, lib_type = self._resolve_logger_info(node, loggers, logger_types, module_path, imports)

            if not logger_name:
                continue

            # Extract message and arguments
            log_call = self._extract_log_call(node, logger_name, method_name)
            if not log_call:
                continue

            # Categorize by library
            self._categorize_log_call(log_call, lib_type, logging_calls, loguru_calls, structlog_calls, django_calls)

    def _resolve_logger_info(
        self,
        node: nodes.Call,
        loggers: dict[str, str],
        logger_types: dict[str, str],
        module_path: str,
        imports: dict[str, str],
    ) -> tuple[str | None, str]:
        """Resolve logger name and library type from a log call.

        Args:
            node: Call node
            loggers: Tracked logger variables
            logger_types: Tracked logger library types
            module_path: Module path
            imports: Detected imports

        Returns:
            Tuple of (logger_name, library_type)
        """
        logger_var = None
        logger_name = None
        lib_type = "logging"  # default

        if isinstance(node.func.expr, nodes.Name):
            logger_var = node.func.expr.name
            logger_name = loggers.get(logger_var)
            lib_type = logger_types.get(logger_var, "logging")

            # Check for direct loguru import: from loguru import logger
            if logger_var == "logger" and logger_var in imports:
                lib_type = imports[logger_var]
                logger_name = "loguru" if lib_type == "loguru" else logger_name

        elif isinstance(node.func.expr, nodes.Attribute):
            # Handle self.logger, cls.logger patterns
            if node.func.expr.attrname in {"logger", "log", "_logger"}:
                logger_name = module_path
                lib_type = "logging"

        # Check for module-level logging (logging.info(), etc.)
        if not logger_name:
            logger_name, lib_type = self._check_module_level_logging(node, module_path)

        return logger_name, lib_type

    def _check_module_level_logging(self, node: nodes.Call, module_path: str) -> tuple[str | None, str]:
        """Check for module-level logging calls.

        Args:
            node: Call node
            module_path: Module path

        Returns:
            Tuple of (logger_name, library_type)
        """
        func_str = safe_as_string(node.func.expr)
        if "logging" in func_str:
            return ("root", "logging")
        elif "loguru" in func_str:
            return ("loguru", "loguru")
        elif "structlog" in func_str:
            return (module_path, "structlog")
        return (None, "logging")

    def _categorize_log_call(
        self,
        log_call: LogCall,
        lib_type: str,
        logging_calls: list[LogCall],
        loguru_calls: list[LogCall],
        structlog_calls: list[LogCall],
        django_calls: list[LogCall],
    ) -> None:
        """Categorize a log call by library type.

        Args:
            log_call: Log call to categorize
            lib_type: Library type
            logging_calls: List for stdlib logging
            loguru_calls: List for loguru
            structlog_calls: List for structlog
            django_calls: List for Django
        """
        if lib_type == "loguru":
            loguru_calls.append(log_call)
        elif lib_type == "structlog":
            structlog_calls.append(log_call)
        elif lib_type == "django":
            django_calls.append(log_call)
        else:  # logging (default)
            logging_calls.append(log_call)

    def _extract_log_call(self, call: nodes.Call, logger_name: str, level: str) -> LogCall | None:
        """Extract log call information from AST node.

        Args:
            call: Call node
            logger_name: Resolved logger name
            level: Log level (method name)

        Returns:
            LogCall object or None if extraction fails
        """
        if not call.args:
            return None

        # Extract message (first argument)
        message_node = call.args[0]
        message = self._extract_message(message_node)
        if not message:
            return None

        # Determine message type
        msg_type = self._detect_message_type(message_node)

        # Extract arguments
        args = self._extract_arguments(call, message_node)

        # Check for sensitive data
        sensitive_patterns: list[str] = []
        if self.check_sensitive:
            _, sensitive_patterns = self._check_sensitive(message, args)

        # Detect code block type
        block_type = self._detect_block_type(call)

        return LogCall(
            logger_name=logger_name,
            lineno=call.lineno or 0,
            level=level,
            message=message,
            args=args,
            type=msg_type,
            block=block_type,
            sensitive_patterns=sensitive_patterns,
        )

    def _extract_message(self, node: nodes.NodeNG) -> str:
        """Extract message string from node.

        Args:
            node: AST node

        Returns:
            Message string or empty string
        """
        if isinstance(node, nodes.Const):
            return str(node.value)
        elif isinstance(node, nodes.JoinedStr):
            # f-string: extract template without f'' wrapper
            return self._extract_fstring_template(node)
        elif isinstance(node, nodes.Name):
            # Variable: try to infer its value
            inferred = infer_value(node).get_if_type(str)
            if inferred is not None:
                return inferred
            # If can't infer, return variable name with backticks
            return f"`{node.name}`"
        else:
            # Try to infer the value first
            inferred = infer_value(node).get_if_type(str)
            if inferred is not None:
                return inferred
            # Fall back to string representation
            return safe_as_string(node)

    def _extract_fstring_template(self, node: nodes.JoinedStr) -> str:
        """Extract f-string template without f'' wrapper.

        Args:
            node: JoinedStr node (f-string)

        Returns:
            Template string with {placeholders}
        """
        parts = []
        for value in node.values:
            if isinstance(value, nodes.Const):
                # Static part - preserve it
                parts.append(str(value.value))
            elif isinstance(value, nodes.FormattedValue):
                # Dynamic part - use {placeholder} format
                value_str = safe_as_string(value.value)
                if value.format_spec:
                    format_spec = safe_as_string(value.format_spec)
                    parts.append(f"{{{value_str}:{format_spec}}}")
                else:
                    parts.append(f"{{{value_str}}}")
            else:
                # Fallback for other node types
                parts.append(f"{{{safe_as_string(value)}}}")
        return "".join(parts)

    def _detect_message_type(self, node: nodes.NodeNG) -> str:
        """Detect message format type.

        Args:
            node: Message node

        Returns:
            Type: 'string', 'fstring', 'percent', 'format'
        """
        if isinstance(node, nodes.JoinedStr):
            return "fstring"
        elif isinstance(node, nodes.BinOp) and node.op == "%":
            return "percent"
        elif isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute) and node.func.attrname == "format":
            return "format"
        return "string"

    def _extract_arguments(self, call: nodes.Call, message_node: nodes.NodeNG) -> list[str]:
        """Extract argument names/expressions from log call.

        Args:
            call: Call node
            message_node: Message node to skip

        Returns:
            List of argument strings
        """
        args = []

        # Get positional arguments after message
        for arg in call.args[1:]:
            arg_str = safe_as_string(arg)
            if arg_str:
                args.append(arg_str)

        # Extract variables from f-string
        if isinstance(message_node, nodes.JoinedStr):
            for value in message_node.values:
                if isinstance(value, nodes.FormattedValue):
                    var_str = safe_as_string(value.value)
                    if var_str and var_str not in args:
                        args.append(var_str)

        return args

    def _detect_block_type(self, node: nodes.Call) -> str:
        """Detect the type of code block containing the log call.

        Args:
            node: Call node

        Returns:
            Block type: function, class, try, except, finally, for, while, if, elif, else, with, module
        """
        # Walk up the parent chain to find the nearest block
        current = node.parent
        while current:
            block_type = self._check_node_type(current, node)
            if block_type == "continue":
                current = current.orelse[0]
                continue
            if block_type:
                return block_type
            current = current.parent
        return "module"

    def _check_node_type(self, current: nodes.NodeNG, node: nodes.Call) -> str | None:
        """Check a single node type and return block type if matched."""
        if isinstance(current, nodes.FunctionDef):
            return "function"
        if isinstance(current, nodes.ClassDef):
            return "class"
        if isinstance(current, nodes.Try):
            return self._detect_try_block(current, node)
        if isinstance(current, (nodes.For, nodes.While)):
            loop_type = "for" if isinstance(current, nodes.For) else "while"
            return self._detect_loop_block(current, node, loop_type)
        if isinstance(current, nodes.If):
            return self._detect_if_block_type(current, node)
        if isinstance(current, nodes.With):
            return "with"
        if isinstance(current, nodes.Module):
            return "module"
        return None

    def _detect_try_block(self, try_node: nodes.Try, node: nodes.Call) -> str:
        """Detect block type within try statement."""
        for handler in try_node.handlers:
            if node in handler.body or any(self._is_ancestor(n, node) for n in handler.body):
                return "except"
        if try_node.finalbody and (
            node in try_node.finalbody or any(self._is_ancestor(n, node) for n in try_node.finalbody)
        ):
            return "finally"
        if try_node.orelse and (node in try_node.orelse or any(self._is_ancestor(n, node) for n in try_node.orelse)):
            return "else"
        return "try"

    def _detect_loop_block(self, loop_node: nodes.For | nodes.While, node: nodes.Call, loop_type: str) -> str:
        """Detect block type within loop statement."""
        if loop_node.orelse and (node in loop_node.orelse or any(self._is_ancestor(n, node) for n in loop_node.orelse)):
            return "else"
        return loop_type

    def _detect_if_block_type(self, if_node: nodes.If, node: nodes.Call) -> str:
        """Detect block type within if statement."""
        if not if_node.orelse:
            return "if"
        # Check if in orelse branch
        if node not in if_node.orelse and not any(self._is_ancestor(n, node) for n in if_node.orelse):
            return "if"
        # Check if orelse is another If (elif)
        if len(if_node.orelse) == 1 and isinstance(if_node.orelse[0], nodes.If):
            return "continue"  # Signal to continue with elif
        return "else"

    def _is_ancestor(self, potential_ancestor: nodes.NodeNG, node: nodes.NodeNG) -> bool:
        """Check if potential_ancestor is an ancestor of node.

        Args:
            potential_ancestor: Potential ancestor node
            node: Node to check

        Returns:
            True if potential_ancestor contains node in its subtree
        """
        current = node.parent
        while current:
            if current is potential_ancestor:
                return True
            current = current.parent
        return False

    def _check_sensitive(self, message: str, args: list[str]) -> tuple[bool, list[str]]:
        """Check if message or arguments contain sensitive data.

        Args:
            message: Log message string
            args: Argument list

        Returns:
            Tuple of (has_sensitive, matched_patterns)
        """
        patterns = []

        # Check message for keywords
        if self._sensitive_pattern.search(message):
            matches = self._sensitive_pattern.findall(message)
            patterns.extend(matches)

        # Check message for JWT tokens
        if self._jwt_pattern.search(message):
            patterns.append("jwt_token")

        # Check argument names for sensitive keywords using pre-compiled patterns
        # Use word boundary matching to avoid false positives (e.g., "key" shouldn't match "keyboard")
        # Consider underscores as word boundaries too (e.g., "key" should match "api_key")
        for arg in args:
            for pattern in self._arg_patterns:
                if pattern.search(arg):
                    patterns.append(arg)
                    break

        return len(patterns) > 0, patterns

    def _calculate_summary(self, results: dict[str, FileLoggingInfo], scan_duration_ms: int) -> LoggingSummary:
        """Calculate summary statistics.

        Args:
            results: Scan results
            scan_duration_ms: Scan duration in milliseconds

        Returns:
            Summary statistics
        """
        total_calls = 0
        by_library: dict[str, int] = {}
        by_level: dict[str, int] = {}
        sensitive_count = 0

        for file_info in results.values():
            for lib_name, calls in [
                ("logging", file_info.logging),
                ("loguru", file_info.loguru),
                ("structlog", file_info.structlog),
                ("django", file_info.django),
            ]:
                count = len(calls)
                if count > 0:
                    by_library[lib_name] = by_library.get(lib_name, 0) + count
                    total_calls += count

                    for call in calls:
                        by_level[call.level] = by_level.get(call.level, 0) + 1
                        if call.sensitive_patterns:
                            sensitive_count += 1

        return LoggingSummary(
            total_count=total_calls,
            total_log_calls=total_calls,
            files_scanned=len(results),
            scan_duration_ms=scan_duration_ms,
            by_library=by_library,
            by_level=by_level,
            sensitive_calls=sensitive_count,
        )
