"""Unit test scanner for detecting pytest and unittest test functions.

This scanner analyzes Python test files to identify test functions, calculate
MD5 hashes of test bodies, count assertions, and resolve test targets based on
root module imports.
"""

import hashlib
import logging
import time
from pathlib import Path

from astroid import nodes

from upcast.common.scanner_base import BaseScanner
from upcast.models.unit_tests import TargetModule, UnitTestInfo, UnitTestOutput, UnitTestSummary

logger = logging.getLogger(__name__)


class UnitTestScanner(BaseScanner[UnitTestOutput]):
    """Scanner for detecting and analyzing unit test functions."""

    def __init__(
        self,
        root_modules: list[str] | None = None,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize unit test scanner.

        Args:
            root_modules: Root module prefixes to match for target resolution (None = all)
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose logging
        """
        # Default patterns to scan only test files
        default_includes = ["test_*.py", "*_test.py"]
        include_patterns = include_patterns or default_includes

        super().__init__(
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            verbose=verbose,
        )
        self.root_modules = root_modules

    def scan(self, path: Path) -> UnitTestOutput:
        """Scan path for unit test functions.

        Args:
            path: Directory or file to scan

        Returns:
            UnitTestOutput with all detected tests grouped by file
        """
        start_time = time.perf_counter()
        files = self.get_files_to_scan(path)

        # Group tests by file path
        tests_by_file: dict[str, list[UnitTestInfo]] = {}

        for file_path in files:
            file_tests = self._scan_file(file_path)
            if file_tests:
                tests_by_file[str(file_path)] = file_tests

        scan_duration_ms = int((time.perf_counter() - start_time) * 1000)
        summary = self._calculate_summary(tests_by_file, scan_duration_ms)

        return UnitTestOutput(summary=summary, tests=tests_by_file)

    def _scan_file(self, file_path: Path) -> list[UnitTestInfo]:
        """Scan a single file for unit test functions.

        Args:
            file_path: Path to the test file

        Returns:
            List of detected test functions
        """
        module = self.parse_file(file_path)
        if not module:
            return []

        tests: list[UnitTestInfo] = []
        module_imports = self._extract_imports(module)

        # Visit all function definitions
        for func_node in module.nodes_of_class(nodes.FunctionDef):
            test_info = self._check_function(func_node, file_path, module_imports)
            if test_info:
                tests.append(test_info)

        if self.verbose and tests:
            logger.info(f"Found {len(tests)} tests in {file_path}")

        return tests

    def _check_function(
        self,
        node: nodes.FunctionDef,
        file_path: Path,
        module_imports: dict[str, str],
    ) -> UnitTestInfo | None:
        """Check if a function is a test function and parse it.

        Args:
            node: Function definition node
            file_path: Path to the test file
            module_imports: Import mappings

        Returns:
            UnitTestInfo if this is a test function, None otherwise
        """
        # Check if this is a test function (starts with test_)
        if not node.name.startswith("test_"):
            return None

        # Check if it's a top-level function or in a test class
        parent = node.parent
        if isinstance(parent, nodes.Module):
            # Top-level test function - valid
            pass
        elif isinstance(parent, nodes.ClassDef):
            # Test method in a class - check if parent is a test class
            if not (parent.name.startswith("Test") or self._is_unittest_testcase(parent)):
                return None
        else:
            # Nested in something else - skip
            return None

        # Parse the test function
        return self._parse_test_function(node, file_path, module_imports)

    def _is_unittest_testcase(self, class_node: nodes.ClassDef) -> bool:
        """Check if a class inherits from unittest.TestCase.

        Args:
            class_node: Class definition node

        Returns:
            True if it's a unittest.TestCase subclass
        """
        for base in class_node.bases:
            try:
                for inferred in base.infer():
                    if hasattr(inferred, "qname") and callable(getattr(inferred, "qname", None)):
                        qname = inferred.qname()  # type: ignore[attr-defined]
                        if "unittest" in qname and "TestCase" in qname:
                            return True
            except Exception:
                # Inference failed, check name directly
                if isinstance(base, nodes.Name) and base.name == "TestCase":
                    return True
                if isinstance(base, nodes.Attribute) and base.attrname == "TestCase":
                    return True
        return False

    def _parse_test_function(
        self,
        func_node: nodes.FunctionDef,
        file_path: Path,
        module_imports: dict[str, str],
    ) -> UnitTestInfo:
        """Parse a test function and extract metadata.

        Args:
            func_node: Function definition node
            file_path: Path to the test file
            module_imports: Import mappings

        Returns:
            UnitTestInfo with all metadata
        """
        name = func_node.name
        line_start = func_node.lineno or 0
        line_end = func_node.end_lineno or line_start

        # Calculate MD5 of normalized body
        body_md5 = self._calculate_body_md5(func_node)

        # Count assertions
        assert_count = self._count_assertions(func_node)

        # Resolve target modules
        targets = self._resolve_targets(func_node, module_imports)

        return UnitTestInfo(
            name=name,
            file=str(file_path),
            line_range=(line_start, line_end),
            body_md5=body_md5,
            assert_count=assert_count,
            targets=targets,
        )

    def _calculate_body_md5(self, func_node: nodes.FunctionDef) -> str:
        """Calculate MD5 hash of normalized function body.

        Args:
            func_node: Function definition node

        Returns:
            MD5 hash as hex string
        """
        # Get function body source
        body_code = func_node.as_string()

        # Normalize code: remove comments and empty lines
        lines = []
        for line in body_code.split("\n"):
            # Remove inline comments (simple approach)
            if "#" in line:
                line = line.split("#")[0]
            line = line.rstrip()
            if line:
                lines.append(line)

        normalized = "\n".join(lines)
        return hashlib.md5(normalized.encode("utf-8")).hexdigest()  # noqa: S324

    def _count_assertions(self, func_node: nodes.FunctionDef) -> int:
        """Count assertion statements in a test function.

        Counts pytest assert statements, unittest self.assert* calls, and pytest.raises.

        Args:
            func_node: Function definition node

        Returns:
            Total assertion count
        """
        count = 0

        # Count pytest assert statements
        for _assert_node in func_node.nodes_of_class(nodes.Assert):
            count += 1

        # Count unittest style assertions (self.assertEqual, etc.)
        for call_node in func_node.nodes_of_class(nodes.Call):
            if (
                isinstance(call_node.func, nodes.Attribute)
                and isinstance(call_node.func.expr, nodes.Name)
                and call_node.func.expr.name == "self"
                and call_node.func.attrname.startswith("assert")
            ):
                count += 1

        # Count pytest.raises context managers
        for with_node in func_node.nodes_of_class(nodes.With):
            for item in with_node.items:
                if (
                    isinstance(item[0], nodes.Call)
                    and isinstance(item[0].func, nodes.Attribute)
                    and item[0].func.attrname == "raises"
                ):
                    count += 1

        return count

    def _extract_imports(self, module: nodes.Module) -> dict[str, str]:
        """Extract import mappings from module.

        Args:
            module: Module node

        Returns:
            Dictionary mapping local names to fully qualified module paths
        """
        imports: dict[str, str] = {}

        # Handle "import X" and "import X as Y"
        for import_node in module.nodes_of_class(nodes.Import):
            for name, alias in import_node.names:
                local_name = alias if alias else name
                imports[local_name] = name

        # Handle "from X import Y" and "from X import Y as Z"
        for import_from in module.nodes_of_class(nodes.ImportFrom):
            module_name = import_from.modname or ""
            for name, alias in import_from.names:
                local_name = alias if alias else name
                if name == "*":
                    # Wildcard import
                    imports[f"*from:{module_name}"] = module_name
                else:
                    # Specific import
                    full_name = f"{module_name}.{name}" if module_name else name
                    imports[local_name] = full_name

        return imports

    def _resolve_targets(
        self,
        func_node: nodes.FunctionDef,
        module_imports: dict[str, str],
    ) -> list[TargetModule]:
        """Resolve test targets based on used names and root modules.

        Args:
            func_node: Function definition node
            module_imports: Import mapping (name -> module)

        Returns:
            List of target modules with symbols
        """
        # Collect all names used in the function
        used_names: set[str] = set()
        for name_node in func_node.nodes_of_class(nodes.Name):
            used_names.add(name_node.name)

        # Map names to modules
        targets: dict[str, set[str]] = {}
        for name in used_names:
            if name not in module_imports:
                continue

            full_path = module_imports[name]
            # Extract module from full path (e.g., "app.math_utils.add" -> "app.math_utils")
            parts = full_path.rsplit(".", 1)
            if len(parts) == 2:
                module, symbol = parts
            else:
                module, symbol = full_path, name

            # Filter by root_modules if specified
            if self.root_modules and not any(module.startswith(root) for root in self.root_modules):
                continue

            # Add to targets
            if module not in targets:
                targets[module] = set()
            targets[module].add(symbol)

        # Convert to TargetModule list
        return [TargetModule(module=module, symbols=sorted(symbols)) for module, symbols in sorted(targets.items())]

    def _calculate_summary(
        self,
        tests_by_file: dict[str, list[UnitTestInfo]],
        scan_duration_ms: int,
    ) -> UnitTestSummary:
        """Calculate summary statistics.

        Args:
            tests_by_file: Tests grouped by file path
            scan_duration_ms: Time taken to scan in milliseconds

        Returns:
            Summary statistics
        """
        total_tests = sum(len(tests) for tests in tests_by_file.values())
        total_files = len(tests_by_file)
        total_assertions = sum(test.assert_count for tests in tests_by_file.values() for test in tests)

        return UnitTestSummary(
            total_count=total_tests,
            files_scanned=total_files,
            scan_duration_ms=scan_duration_ms,
            total_tests=total_tests,
            total_files=total_files,
            total_assertions=total_assertions,
        )
