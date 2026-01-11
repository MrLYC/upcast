"""Data models for signal scanner.

Models extracted from upcast/scanners/signals.py for shared use.
"""

from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class SignalUsage(BaseModel):
    """Represents a single usage of a signal (send or receive).

    Attributes:
        file: Relative path from project root
        lineno: Line number (1-based)
        handler: Handler function name (for receivers)
        sender: Sender class if specified
        statement: Source code snippet
    """

    file: str = Field(description="Relative path from project root")
    lineno: int = Field(ge=1, description="Line number (1-based)")
    handler: str | None = Field(None, description="Handler function name")
    sender: str | None = Field(None, description="Sender class if specified")
    statement: str | None = Field(None, description="Source code snippet")


class SignalInfo(BaseModel):
    """Information about a single signal and its usage.

    Attributes:
        signal: Signal name (e.g., 'post_save', 'task_success')
        type: Framework type ('django' or 'celery')
        category: Signal category (e.g., 'model_signals', 'task_signals')
        receivers: List of signal receivers/handlers
        senders: List of signal sends
        status: Signal status (e.g., 'unused' for defined but unused signals)
    """

    signal: str = Field(description="Signal name")
    type: str = Field(description="Framework type (django/celery)")
    category: str = Field(description="Signal category")
    receivers: list[SignalUsage] = Field(description="Signal receivers/handlers")
    senders: list[SignalUsage] = Field(description="Signal sends")
    status: str | None = Field(None, description="Signal status (e.g., 'unused')")


class SignalSummary(ScannerSummary):
    """Summary statistics for signal scanner.

    Extends base ScannerSummary with signal-specific counts.

    Attributes:
        django_receivers: Number of Django signal receivers
        django_senders: Number of Django signal sends
        celery_receivers: Number of Celery signal receivers
        celery_senders: Number of Celery signal sends
        custom_signals_defined: Number of custom signals defined
        unused_custom_signals: Number of custom signals defined but not used
    """

    django_receivers: int = Field(ge=0, description="Django signal receivers")
    django_senders: int = Field(ge=0, description="Django signal sends")
    celery_receivers: int = Field(ge=0, description="Celery signal receivers")
    celery_senders: int = Field(ge=0, description="Celery signal sends")
    custom_signals_defined: int = Field(ge=0, description="Custom signals defined")
    unused_custom_signals: int = Field(ge=0, description="Unused custom signals")


class SignalOutput(ScannerOutput[list[SignalInfo]]):
    """Complete output from signal scanner.

    Attributes:
        summary: Signal scan summary statistics
        results: List of SignalInfo objects
    """

    summary: SignalSummary
    results: list[SignalInfo]
