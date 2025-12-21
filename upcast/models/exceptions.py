"""Data models for exception handler scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class ExceptClause(BaseModel):
    """An except clause in a try-except block.

    Attributes:
        line: Line number
        exception_types: Exception types handled
        lines: Number of lines in clause
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

    line: int = Field(..., ge=1, description="Line number")
    exception_types: list[str] = Field(default_factory=list, description="Exception types handled")
    lines: int = Field(ge=0, description="Number of lines in clause")
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


class ElseClause(BaseModel):
    """An else clause in a try-except block.

    Attributes:
        line: Line number
        lines: Number of lines in clause
    """

    line: int = Field(..., ge=1, description="Line number")
    lines: int = Field(ge=0, description="Number of lines")


class FinallyClause(BaseModel):
    """A finally clause in a try-except block.

    Attributes:
        line: Line number
        lines: Number of lines in clause
    """

    line: int = Field(..., ge=1, description="Line number")
    lines: int = Field(ge=0, description="Number of lines")


class ExceptionHandler(BaseModel):
    """A complete try-except block.

    Attributes:
        file: File path
        lineno: Start line number
        end_lineno: End line number
        try_lines: Number of lines in try block
        except_clauses: List of except clauses
        else_clause: Optional else clause
        finally_clause: Optional finally clause
    """

    file: str = Field(..., description="File path")
    lineno: int = Field(..., ge=1, description="Start line")
    end_lineno: int = Field(..., ge=1, description="End line")
    try_lines: int = Field(ge=0, description="Number of lines in try block")
    except_clauses: list[ExceptClause] = Field(..., description="Except clauses")
    else_clause: ElseClause | None = Field(None, description="Else clause")
    finally_clause: FinallyClause | None = Field(None, description="Finally clause")


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
    results: list[ExceptionHandler] = Field(..., alias="exception_handlers", description="Exception handlers")
