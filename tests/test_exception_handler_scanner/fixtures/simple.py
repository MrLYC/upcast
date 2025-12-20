# ruff: noqa
"""Simple try/except patterns for testing."""

import logging

logger = logging.getLogger(__name__)


def simple_try_except():
    """Basic try/except with logging."""
    try:
        result = 10 / 0
        return result
    except ValueError:
        logger.error("ValueError occurred")
        return None


def bare_except_with_pass():
    """Bare except with pass statement."""
    try:
        value = int("not a number")
    except:  # noqa: E722
        pass


def multiple_exception_types():
    """Multiple exception types in one except clause."""
    try:
        data = {}
        value = data["key"]
    except (KeyError, ValueError):
        logger.warning("Key or value error")
        return None
