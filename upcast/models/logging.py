"""Data models for logging scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class LogCall(BaseModel):
    """A single logging call detected in source code.

    Attributes:
        logger_name: Resolved logger name (e.g., 'root', 'myapp.services.auth')
        lineno: Line number where the call occurs
        level: Log level (debug, info, warning, error, critical)
        message: Complete message string
        args: List of argument names/expressions passed to the log call
        type: Message format type ('string', 'fstring', 'percent', 'format')
        block: Code block type where the log call is located
        sensitive_patterns: List of matched sensitive patterns/keywords
    """

    logger_name: str = Field(description="Resolved logger name")
    lineno: int = Field(ge=1, description="Line number")
    level: str = Field(description="Log level")
    message: str = Field(description="Complete message string")
    args: list[str] = Field(default_factory=list, description="Argument names/expressions")
    type: str = Field(description="Message format type")
    block: str = Field(
        description="Code block type: function, class, try, except, finally, for, while, if, elif, else, with, module"
    )
    sensitive_patterns: list[str] = Field(default_factory=list, description="Matched sensitive patterns")


class FileLoggingInfo(BaseModel):
    """Logging information for a single file, organized by library.

    Attributes:
        logging: Calls using Python standard library logging
        loguru: Calls using loguru library
        structlog: Calls using structlog library
        django: Calls using Django logging utilities
    """

    logging: list[LogCall] = Field(default_factory=list, description="Standard library logging calls")
    loguru: list[LogCall] = Field(default_factory=list, description="Loguru calls")
    structlog: list[LogCall] = Field(default_factory=list, description="Structlog calls")
    django: list[LogCall] = Field(default_factory=list, description="Django logging calls")


class LoggingSummary(ScannerSummary):
    """Summary statistics for logging analysis.

    Attributes:
        total_log_calls: Total number of logging calls detected
        files_scanned: Number of files scanned
        scan_duration_ms: Scan duration in milliseconds
        by_library: Count of calls per library
        by_level: Count of calls per log level
        sensitive_calls: Number of calls with sensitive data
    """

    total_log_calls: int = Field(ge=0, description="Total logging calls")
    by_library: dict[str, int] = Field(default_factory=dict, description="Calls per library")
    by_level: dict[str, int] = Field(default_factory=dict, description="Calls per level")
    sensitive_calls: int = Field(ge=0, description="Calls with sensitive data")


class LoggingOutput(ScannerOutput[dict[str, FileLoggingInfo]]):
    """Complete output from logging scanner.

    Attributes:
        summary: Summary statistics
        results: Logging information keyed by file path
    """

    summary: LoggingSummary
    results: dict[str, FileLoggingInfo] = Field(description="Logging info by file")
