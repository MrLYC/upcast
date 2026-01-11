"""Data models for exception handler scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class ExceptionBlock(BaseModel):
    """An except clause in a try-except block.

    Attributes:
        lineno: Line number
        lines: Number of lines in clause
        exceptions: Exception types handled
        log_debug_count: Number of log.debug() calls
        log_info_count: Number of log.info() calls
        log_warning_count: Number of log.warning() calls
        log_error_count: Number of log.error() calls
        log_exception_count: Number of log.exception() calls
        log_critical_count: Number of log.critical() calls
        pass_count: Number of pass statements
        return_count: Number of return statements
        break_count: Number of break statements
        continue_count: Number of continue statements
        raise_count: Number of raise statements
    """

    lineno: int | None = Field(ge=1, description="Line number")
    lines: int = Field(ge=0, description="Number of lines in clause")
    exceptions: list[str] = Field(description="Exception types handled")
    log_debug_count: int = Field(default=0, ge=0, description="log.debug() calls")
    log_info_count: int = Field(default=0, ge=0, description="log.info() calls")
    log_warning_count: int = Field(default=0, ge=0, description="log.warning() calls")
    log_error_count: int = Field(default=0, ge=0, description="log.error() calls")
    log_exception_count: int = Field(default=0, ge=0, description="log.exception() calls")
    log_critical_count: int = Field(default=0, ge=0, description="log.critical() calls")
    pass_count: int = Field(default=0, ge=0, description="pass statements")
    return_count: int = Field(default=0, ge=0, description="return statements")
    break_count: int = Field(default=0, ge=0, description="break statements")
    continue_count: int = Field(default=0, ge=0, description="continue statements")
    raise_count: int = Field(default=0, ge=0, description="raise statements")


class ExceptionHandler(BaseModel):
    """A complete try-except block.

    Attributes:
        file: File path
        try_lineno: try statement start line number
        try_lines: Number of lines in try block
        else_lineno: else statement start line number (null if no else)
        else_lines: Number of lines in else block (null if no else)
        finally_lineno: finally statement start line number (null if no finally)
        finally_lines: Number of lines in finally block (null if no finally)
        nested_exceptions: Whether there are nested exception handlers
        exception_blocks: List of except clauses
    """

    file: str = Field(description="File path")
    try_lineno: int | None = Field(ge=1, description="try statement start line")
    try_lines: int | None = Field(ge=0, description="Number of lines in try block")
    else_lineno: int | None = Field(None, description="else statement start line")
    else_lines: int | None = Field(None, ge=0, description="Number of lines in else block")
    finally_lineno: int | None = Field(None, description="finally statement start line")
    finally_lines: int | None = Field(None, ge=0, description="Number of lines in finally block")
    nested_exceptions: bool = Field(default=False, description="Has nested exception handlers")
    exception_blocks: list[ExceptionBlock] = Field(description="Except clauses")


class ExceptionHandlerSummary(ScannerSummary):
    """Summary statistics for exception handlers.

    Attributes:
        total_handlers: Total number of try-except blocks
        total_except_clauses: Total number of except clauses
    """

    total_handlers: int = Field(ge=0, description="Total try-except blocks")
    total_except_clauses: int = Field(ge=0, description="Total except clauses")


class ExceptionHandlerOutput(ScannerOutput[list[ExceptionHandler]]):
    """Complete output from exception handler scanner.

    Attributes:
        summary: Summary statistics
        results: List of exception handlers
    """

    summary: ExceptionHandlerSummary
    results: list[ExceptionHandler] = Field(description="Exception handlers")
