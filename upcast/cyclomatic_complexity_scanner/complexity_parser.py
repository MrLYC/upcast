"""Parser for cyclomatic complexity calculation."""

from dataclasses import dataclass

from astroid import nodes


@dataclass
class ComplexityResult:
    """Result of complexity analysis for a single function."""

    name: str
    line: int
    end_line: int
    complexity: int
    severity: str
    description: str | None
    signature: str
    is_async: bool
    is_method: bool
    class_name: str | None
    code: str  # Complete function source code
    comment_lines: int  # Number of comment lines in function
    code_lines: int  # Total lines including code and comments


class ComplexityVisitor:
    """Calculate cyclomatic complexity by counting decision points."""

    def __init__(self) -> None:
        """Initialize complexity visitor."""
        self.complexity = 1  # Base complexity

    def visit(self, node: nodes.NodeNG) -> None:
        """Visit a node and its children."""
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node: nodes.NodeNG) -> None:
        """Visit all child nodes."""
        for child in node.get_children():
            self.visit(child)

    def visit_If(self, node: nodes.If) -> None:
        """Visit if statement: +1 for if, +1 per elif."""
        self.complexity += 1
        # Count boolean operators in condition
        self.complexity += self._count_bool_ops(node.test)
        self.generic_visit(node)

    def visit_For(self, node: nodes.For) -> None:
        """Visit for loop: +1."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: nodes.While) -> None:
        """Visit while loop: +1, plus boolean operators in condition."""
        self.complexity += 1
        self.complexity += self._count_bool_ops(node.test)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: nodes.ExceptHandler) -> None:
        """Visit except handler: +1."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: nodes.BoolOp) -> None:
        """Visit boolean operation: +1 per and/or operator."""
        # BoolOp contains multiple values connected by and/or
        # Number of operators = len(values) - 1
        # Skip counting here, handled by _count_bool_ops in parent contexts
        self.generic_visit(node)

    def visit_IfExp(self, node: nodes.IfExp) -> None:
        """Visit ternary expression: +1."""
        self.complexity += 1
        # Count boolean operators in condition
        self.complexity += self._count_bool_ops(node.test)
        self.generic_visit(node)

    def visit_Comprehension(self, node: nodes.Comprehension) -> None:
        """Visit comprehension: +1 per if clause."""
        # Count if clauses in comprehension
        self.complexity += len(node.ifs)
        # Count boolean operators in each if clause
        for if_clause in node.ifs:
            self.complexity += self._count_bool_ops(if_clause)
        self.generic_visit(node)

    def visit_Assert(self, node: nodes.Assert) -> None:
        """Visit assert statement: +1 for assert itself."""
        self.complexity += 1
        if node.test:
            self.complexity += self._count_bool_ops(node.test)
        self.generic_visit(node)

    def _count_bool_ops(self, node: nodes.NodeNG) -> int:
        """Count boolean operators (and/or) in an expression."""
        count = 0
        for child in node.nodes_of_class(nodes.BoolOp):
            # Each BoolOp has len(values) - 1 operators
            count += len(child.values) - 1
        return count


def calculate_complexity(node: nodes.FunctionDef) -> int:
    """Calculate cyclomatic complexity for a function.

    Args:
        node: Function definition node

    Returns:
        Cyclomatic complexity value

    Examples:
        >>> def simple_func():
        ...     return 42
        >>> calculate_complexity(func_node)  # Base complexity
        1

        >>> def complex_func(x):
        ...     if x > 0:  # +1
        ...         if x > 10:  # +1
        ...             return "big"
        ...     for i in range(x):  # +1
        ...         if i % 2:  # +1
        ...             print(i)
        ...     return "done"
        >>> calculate_complexity(func_node)
        5
    """
    visitor = ComplexityVisitor()
    visitor.visit(node)
    return visitor.complexity


def assign_severity(complexity: int) -> str:
    """Assign severity level based on complexity value.

    Args:
        complexity: Cyclomatic complexity value

    Returns:
        Severity level string

    Severity levels:
        - healthy: complexity ≤ 5
        - acceptable: 6 ≤ complexity ≤ 10
        - warning: 11 ≤ complexity ≤ 15
        - high_risk: 16 ≤ complexity ≤ 20
        - critical: complexity > 20

    Examples:
        >>> assign_severity(3)
        'healthy'
        >>> assign_severity(12)
        'warning'
        >>> assign_severity(25)
        'critical'
    """
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


def filter_by_threshold(results: list[ComplexityResult], threshold: int = 11) -> list[ComplexityResult]:
    """Filter results by complexity threshold.

    Args:
        results: List of complexity results
        threshold: Minimum complexity to include (default: 11)

    Returns:
        Filtered list of results

    Examples:
        >>> results = [
        ...     ComplexityResult(name="func1", complexity=5, ...),
        ...     ComplexityResult(name="func2", complexity=15, ...),
        ... ]
        >>> filtered = filter_by_threshold(results, threshold=10)
        >>> len(filtered)
        1
        >>> filtered[0].name
        'func2'
    """
    return [r for r in results if r.complexity >= threshold]
