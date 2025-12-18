"""Checker for collecting exception handlers from Python files."""

from pathlib import Path

from astroid import nodes, parse

from upcast.exception_handler_scanner.handler_parser import ExceptionHandler, parse_try_block


class ExceptionHandlerChecker:
    """Visitor class to collect exception handlers from Python AST."""

    def __init__(self, base_path: Path):
        """Initialize the checker.

        Args:
            base_path: Base directory path for calculating relative file paths
        """
        self.base_path = base_path
        self.handlers: list[ExceptionHandler] = []

    def visit_try(self, node: nodes.Try, file_path: str) -> None:
        """Visit a try block and extract handler information.

        Args:
            node: The try block node
            file_path: Relative path to the file
        """
        handler = parse_try_block(node, file_path)
        self.handlers.append(handler)

    def check_file(self, file_path: Path) -> None:
        """Process a single Python file.

        Args:
            file_path: Path to the Python file to check
        """
        try:
            with file_path.open("r", encoding="utf-8") as f:
                content = f.read()

            tree = parse(content)
            relative_path = str(file_path.relative_to(self.base_path))

            # Visit all try blocks in the file
            for node in tree.nodes_of_class(nodes.Try):
                self.visit_try(node, relative_path)

        except Exception as e:
            # Skip files that cannot be parsed
            import logging

            logging.debug(f"Failed to parse {file_path}: {e}")

    def get_handlers(self) -> list[ExceptionHandler]:
        """Get all collected exception handlers.

        Returns:
            List of ExceptionHandler objects
        """
        return self.handlers

    def get_summary(self) -> dict:
        """Calculate summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        total_try_blocks = len(self.handlers)
        total_except_clauses = sum(len(h.except_clauses) for h in self.handlers)

        # Count bare excepts
        bare_excepts = sum(1 for h in self.handlers for clause in h.except_clauses if not clause.exception_types)

        # Count except blocks with specific control flow
        except_with_pass = sum(1 for h in self.handlers for clause in h.except_clauses if clause.pass_count > 0)
        except_with_return = sum(1 for h in self.handlers for clause in h.except_clauses if clause.return_count > 0)
        except_with_raise = sum(1 for h in self.handlers for clause in h.except_clauses if clause.raise_count > 0)

        # Count logging
        total_log_calls = sum(
            clause.log_debug_count
            + clause.log_info_count
            + clause.log_warning_count
            + clause.log_error_count
            + clause.log_exception_count
            + clause.log_critical_count
            for h in self.handlers
            for clause in h.except_clauses
        )

        except_without_logging = sum(
            1
            for h in self.handlers
            for clause in h.except_clauses
            if (
                clause.log_debug_count == 0
                and clause.log_info_count == 0
                and clause.log_warning_count == 0
                and clause.log_error_count == 0
                and clause.log_exception_count == 0
                and clause.log_critical_count == 0
            )
        )

        return {
            "total_try_blocks": total_try_blocks,
            "total_except_clauses": total_except_clauses,
            "bare_excepts": bare_excepts,
            "except_with_pass": except_with_pass,
            "except_with_return": except_with_return,
            "except_with_raise": except_with_raise,
            "total_log_calls": total_log_calls,
            "except_without_logging": except_without_logging,
        }
