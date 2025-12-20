"""Checker for cyclomatic complexity analysis."""

from pathlib import Path

from astroid import MANAGER, nodes

from upcast.common.code_utils import (
    count_comment_lines,
    extract_function_code,
    get_code_lines,
)
from upcast.cyclomatic_complexity_scanner.complexity_parser import (
    ComplexityResult,
    assign_severity,
    calculate_complexity,
    filter_by_threshold,
)


def get_default_exclude_patterns() -> list[str]:
    """Get default test file exclusion patterns.

    Returns:
        List of glob patterns for test files
    """
    return [
        "tests/**",
        "**/tests/**",
        "test_*.py",
        "*_test.py",
        "**/test_*.py",
    ]


class ComplexityChecker:
    """Check Python files for high cyclomatic complexity."""

    def __init__(
        self,
        threshold: int = 11,
        include_tests: bool = False,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
    ) -> None:
        """Initialize complexity checker.

        Args:
            threshold: Minimum complexity to report (default: 11)
            include_tests: Include test files (default: False)
            include_patterns: Additional include patterns
            exclude_patterns: Additional exclude patterns
        """
        self.threshold = threshold
        self.include_tests = include_tests
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []

    def _should_exclude(self, file_path: str) -> bool:
        """Check if file should be excluded.

        Args:
            file_path: File path to check

        Returns:
            True if file should be excluded
        """
        if self.include_tests:
            return False

        path = Path(file_path)

        # Check against default test patterns
        return any(path.match(pattern) for pattern in get_default_exclude_patterns())

    def _extract_function_metadata(
        self, node: nodes.FunctionDef, parent_class: str | None = None
    ) -> ComplexityResult | None:
        """Extract metadata and calculate complexity for a function.

        Args:
            node: Function definition node
            parent_class: Parent class name if this is a method

        Returns:
            ComplexityResult or None if extraction fails
        """
        try:
            # Calculate complexity
            complexity = calculate_complexity(node)

            # Extract source code
            code = extract_function_code(node)
            if not code:
                return None

            # Count comment lines
            comment_lines = count_comment_lines(code)

            # Get total code lines
            code_lines = get_code_lines(node)

            # Extract docstring (first line only)
            description = None
            if node.doc_node:
                doc = node.doc_node.value
                if doc:
                    description = doc.split("\n")[0].strip()

            # Build signature (merge multi-line signatures into one line, skip decorators)
            lines = node.as_string().split("\n")
            signature_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped:
                    # Skip decorator lines (start with @)
                    if stripped.startswith("@"):
                        continue
                    signature_lines.append(stripped)
                    if ":" in stripped:  # Found end of signature
                        break
            signature = " ".join(signature_lines) if signature_lines else ""

            # Determine severity
            severity = assign_severity(complexity)

            return ComplexityResult(
                name=node.name,
                line=node.lineno,
                end_line=node.end_lineno or node.lineno,
                complexity=complexity,
                severity=severity,
                description=description,
                signature=signature,
                is_async=isinstance(node, nodes.AsyncFunctionDef),
                is_method=parent_class is not None,
                class_name=parent_class,
                code=code,
                comment_lines=comment_lines,
                code_lines=code_lines,
            )
        except Exception:
            return None

    def check_file(self, file_path: str) -> list[ComplexityResult]:
        """Check a single Python file for complexity.

        Args:
            file_path: Path to Python file

        Returns:
            List of complexity results above threshold
        """
        if self._should_exclude(file_path):
            return []

        try:
            # Parse file with astroid
            module = MANAGER.ast_from_file(file_path)

            results: list[ComplexityResult] = []

            # Find all functions and methods
            for node in module.nodes_of_class((nodes.FunctionDef, nodes.AsyncFunctionDef)):
                # Determine if this is a method
                parent_class = None
                if node.parent and isinstance(node.parent, nodes.ClassDef):
                    parent_class = node.parent.name

                result = self._extract_function_metadata(node, parent_class)
                if result:
                    results.append(result)

            # Filter by threshold
            return filter_by_threshold(results, self.threshold)

        except Exception:
            # Silently skip files with errors
            return []

    def check_files(self, file_paths: list[str], base_path: str | None = None) -> dict[str, list[ComplexityResult]]:
        """Check multiple Python files.

        Args:
            file_paths: List of file paths
            base_path: Base path for relative paths (optional)

        Returns:
            Dictionary mapping module paths to results
        """
        results_by_module: dict[str, list[ComplexityResult]] = {}

        for file_path in file_paths:
            results = self.check_file(file_path)
            if results:
                # Convert to relative path if base_path provided
                if base_path:
                    try:
                        module_path = str(Path(file_path).relative_to(base_path))
                    except ValueError:
                        module_path = file_path
                else:
                    module_path = file_path

                # Sort results by line number
                results.sort(key=lambda r: r.line)
                results_by_module[module_path] = results

        return results_by_module
