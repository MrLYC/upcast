"""Export functions for exception handler scanner output."""

from upcast.common.export import export_to_json, export_to_yaml, export_to_yaml_string
from upcast.exception_handler_scanner.handler_parser import ExceptionHandler


def format_handler_output(handlers: list[ExceptionHandler], summary: dict) -> dict:
    """Format exception handlers for output.

    Args:
        handlers: List of ExceptionHandler objects
        summary: Summary statistics dictionary

    Returns:
        Dictionary ready for YAML/JSON export
    """
    formatted_handlers = []

    for handler in handlers:
        # Format except clauses
        formatted_clauses = []
        for clause in handler.except_clauses:
            formatted_clauses.append({
                "line": clause.line,
                "exception_types": clause.exception_types,
                "lines": clause.lines,
                "log_debug_count": clause.log_debug_count,
                "log_info_count": clause.log_info_count,
                "log_warning_count": clause.log_warning_count,
                "log_error_count": clause.log_error_count,
                "log_exception_count": clause.log_exception_count,
                "log_critical_count": clause.log_critical_count,
                "pass_count": clause.pass_count,
                "return_count": clause.return_count,
                "break_count": clause.break_count,
                "continue_count": clause.continue_count,
                "raise_count": clause.raise_count,
            })

        # Format else clause
        else_clause = None
        if handler.else_clause:
            else_clause = {
                "line": handler.else_clause.line,
                "lines": handler.else_clause.lines,
            }

        # Format finally clause
        finally_clause = None
        if handler.finally_clause:
            finally_clause = {
                "line": handler.finally_clause.line,
                "lines": handler.finally_clause.lines,
            }

        formatted_handlers.append({
            "location": handler.location,
            "try_lines": handler.try_lines,
            "except_clauses": formatted_clauses,
            "else_clause": else_clause,
            "finally_clause": finally_clause,
        })

    return {
        "exception_handlers": formatted_handlers,
        "summary": summary,
    }


def export_exception_handlers(
    handlers: list[ExceptionHandler],
    summary: dict,
    output_path: str | None = None,
    format_type: str = "yaml",
) -> str:
    """Export exception handlers to YAML or JSON.

    Args:
        handlers: List of ExceptionHandler objects
        summary: Summary statistics dictionary
        output_path: Optional file path to write output
        format_type: Output format ('yaml' or 'json')

    Returns:
        Formatted output string
    """
    data = format_handler_output(handlers, summary)

    if format_type == "json":
        return export_to_json(data, output_path)

    if output_path:
        export_to_yaml(data, output_path)
        return ""
    return export_to_yaml_string(data)
