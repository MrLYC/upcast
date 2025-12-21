"""Cyclomatic complexity scanner implementation with Pydantic models."""

from pathlib import Path

from astroid import nodes

from upcast.common.code_utils import extract_function_code
from upcast.common.scanner_base import BaseScanner
from upcast.models.complexity import ComplexityOutput, ComplexityResult, ComplexitySummary


class ComplexityScanner(BaseScanner[ComplexityOutput]):
    """Scanner for cyclomatic complexity analysis.

    Detects functions with high cyclomatic complexity that may need refactoring.
    """

    def __init__(
        self,
        threshold: int = 11,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize complexity scanner.

        Args:
            threshold: Minimum complexity to report (default: 11)
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose output
        """
        super().__init__(include_patterns, exclude_patterns, verbose)
        self.threshold = threshold

    def scan(self, path: Path) -> ComplexityOutput:
        """Scan for high complexity functions."""
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent

        modules: dict[str, list[ComplexityResult]] = {}

        for file_path in files:
            module = self.parse_file(file_path)
            if not module:
                continue

            results = self._scan_module(module)
            if results:
                from upcast.common.file_utils import get_relative_path_str

                rel_path = get_relative_path_str(file_path, base_path)
                results.sort(key=lambda r: r.line)
                modules[rel_path] = results

        summary = self._calculate_summary(modules)
        return ComplexityOutput(summary=summary, modules=modules)

    def _scan_module(self, module: nodes.Module) -> list[ComplexityResult]:
        """Scan a module for high complexity functions."""
        results: list[ComplexityResult] = []

        for node in module.nodes_of_class((nodes.FunctionDef, nodes.AsyncFunctionDef)):
            parent_class = None
            if node.parent and isinstance(node.parent, nodes.ClassDef):
                parent_class = node.parent.name

            result = self._analyze_function(node, parent_class)
            if result and result.complexity >= self.threshold:
                results.append(result)

        return results

    def _analyze_function(self, node: nodes.FunctionDef, parent_class: str | None) -> ComplexityResult | None:
        """Analyze a function for complexity."""
        try:
            complexity = self._calculate_complexity(node)
            code = extract_function_code(node)
            if not code:
                return None

            severity = self._assign_severity(complexity)
            message = f"Complexity {complexity} exceeds threshold {self.threshold}"

            return ComplexityResult(
                name=node.name,
                line=node.lineno,
                end_line=node.end_lineno or node.lineno,
                complexity=complexity,
                severity=severity,
                message=message,
            )
        except Exception:
            return None

    def _calculate_complexity(self, node: nodes.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        for child in node.nodes_of_class((
            nodes.If,
            nodes.For,
            nodes.While,
            nodes.ExceptHandler,
            nodes.IfExp,
            nodes.Assert,
        )):
            complexity += 1

            # Count boolean operators in conditions
            if hasattr(child, "test") and child.test:
                complexity += self._count_bool_ops(child.test)

        # Count comprehension if clauses
        for comp in node.nodes_of_class(nodes.Comprehension):
            complexity += len(comp.ifs)
            for if_clause in comp.ifs:
                complexity += self._count_bool_ops(if_clause)

        return complexity

    def _count_bool_ops(self, node: nodes.NodeNG) -> int:
        """Count boolean operators (and/or) in expression."""
        count = 0
        for child in node.nodes_of_class(nodes.BoolOp):
            count += len(child.values) - 1
        return count

    def _assign_severity(self, complexity: int) -> str:
        """Assign severity level based on complexity."""
        if complexity <= 5:
            return "healthy"
        elif complexity <= 10:
            return "acceptable"
        elif complexity <= 15:
            return "warning"
        elif complexity <= 20:
            return "high_risk"
        else:
            return "critical"

    def _calculate_summary(self, modules: dict[str, list[ComplexityResult]]) -> ComplexitySummary:
        """Calculate summary statistics."""
        all_results = [r for results in modules.values() for r in results]
        by_severity: dict[str, int] = {}
        for result in all_results:
            by_severity[result.severity] = by_severity.get(result.severity, 0) + 1

        return ComplexitySummary(
            total_count=len(all_results),
            files_scanned=len(modules),
            high_complexity_count=len(all_results),
            by_severity=by_severity,
        )
