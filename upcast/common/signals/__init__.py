"""Common signal analysis utilities.

This package contains utilities for parsing and detecting Django and Celery signal patterns.

Available modules:
- signal_parser.py: Signal pattern parsing (decorators, connects, sends)
- signal_checker.py: AST visitor for signal detection
"""

from upcast.common.signals.signal_checker import SignalChecker
from upcast.common.signals.signal_parser import (
    SignalUsage,
    categorize_celery_signal,
    categorize_django_signal,
    parse_celery_connect_decorator,
    parse_custom_signal_definition,
    parse_receiver_decorator,
    parse_signal_connect_method,
    parse_signal_send,
)

__all__ = [
    "SignalChecker",
    "SignalUsage",
    "categorize_celery_signal",
    "categorize_django_signal",
    "parse_celery_connect_decorator",
    "parse_custom_signal_definition",
    "parse_receiver_decorator",
    "parse_signal_connect_method",
    "parse_signal_send",
]
