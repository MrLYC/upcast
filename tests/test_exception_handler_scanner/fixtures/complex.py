# ruff: noqa
"""Complex exception handling patterns."""

import logging

logger = logging.getLogger(__name__)


def try_except_else_finally():
    """Complete try/except/else/finally block."""
    try:
        result = 10 / 2
    except ZeroDivisionError:
        logger.error("Cannot divide by zero")
        return None
    else:
        logger.info("Division successful")
        return result
    finally:
        logger.debug("Cleanup")


def multiple_except_clauses():
    """Multiple except clauses handling different exceptions."""
    try:
        data = {}
        value = data["key"]
        result = int(value)
    except KeyError:
        logger.error("Key not found")
        return None
    except ValueError:
        logger.error("Invalid value")
        return None
    except Exception:
        logger.exception("Unexpected error")
        raise


def nested_try_blocks():
    """Nested try/except blocks."""
    try:
        data = {}
        try:
            value = data["key"]
        except KeyError:
            logger.warning("Key not found, using default")
            value = "default"
        result = int(value)
    except ValueError:
        logger.error("Invalid value")
        return None
