"""Signal scanner for detecting Django and Celery signal patterns.

.. deprecated::
    This module is deprecated. Use :mod:`upcast.scanners.signal` instead.
    The old implementation will be removed in a future release.
"""

import warnings

from upcast.signal_scanner.checker import SignalChecker
from upcast.signal_scanner.cli import scan_signals
from upcast.signal_scanner.signal_parser import SignalUsage

__all__ = ["SignalChecker", "SignalUsage", "scan_signals"]

# Issue deprecation warning when module is imported
warnings.warn(
    "upcast.signal_scanner is deprecated. "
    "Use upcast.scanners.signal instead. "
    "The old implementation will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2,
)
