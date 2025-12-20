"""Exception handler scanner for detecting try/except patterns in Python code."""

from upcast.exception_handler_scanner.checker import ExceptionHandlerChecker
from upcast.exception_handler_scanner.cli import scan_exception_handlers
from upcast.exception_handler_scanner.handler_parser import (
    BlockInfo,
    ExceptionClause,
    ExceptionHandler,
)

__all__ = [
    "BlockInfo",
    "ExceptionClause",
    "ExceptionHandler",
    "ExceptionHandlerChecker",
    "scan_exception_handlers",
]
