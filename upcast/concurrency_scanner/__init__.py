"""Concurrency pattern scanner.

This module provides tools to detect and analyze concurrency patterns in Python code,
including asyncio, threading, and multiprocessing usage.
"""

from upcast.concurrency_scanner.checker import ConcurrencyChecker
from upcast.concurrency_scanner.cli import scan_concurrency

__all__ = ["scan_concurrency", "ConcurrencyChecker"]
