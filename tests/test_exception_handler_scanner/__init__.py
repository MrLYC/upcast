"""Pytest fixtures for exception handler scanner tests."""

import pytest
from pathlib import Path

from upcast.scanners.exceptions import ExceptionHandlerScanner


@pytest.fixture
def scanner():
    """Create an ExceptionHandlerScanner instance."""
    return ExceptionHandlerScanner(verbose=False)


@pytest.fixture
def simple_try_except():
    """Simple try-except block."""
    return """
try:
    risky_operation()
except ValueError:
    handle_error()
"""


@pytest.fixture
def multiple_except_clauses():
    """Try block with multiple except clauses."""
    return """
try:
    operation()
except ValueError:
    handle_value_error()
except KeyError:
    handle_key_error()
except Exception:
    handle_generic()
"""


@pytest.fixture
def try_except_else():
    """Try-except with else clause."""
    return """
try:
    operation()
except ValueError:
    handle_error()
else:
    success_handler()
"""


@pytest.fixture
def try_except_finally():
    """Try-except with finally clause."""
    return """
try:
    operation()
except ValueError:
    handle_error()
finally:
    cleanup()
"""


@pytest.fixture
def try_except_else_finally():
    """Try-except with both else and finally."""
    return """
try:
    operation()
except ValueError:
    handle_error()
else:
    success_handler()
finally:
    cleanup()
"""


@pytest.fixture
def except_with_logging():
    """Except clause with logging calls."""
    return """
import logging

logger = logging.getLogger(__name__)

try:
    operation()
except ValueError as e:
    logger.error("Error occurred: %s", e)
    logger.exception("Full traceback")
"""


@pytest.fixture
def except_with_control_flow():
    """Except clause with control flow statements."""
    return """
def process():
    try:
        operation()
    except ValueError:
        return None
    except KeyError:
        pass
    except Exception:
        raise
"""


@pytest.fixture
def bare_except():
    """Bare except clause (catches all)."""
    return """
try:
    operation()
except:
    handle_all_errors()
"""


@pytest.fixture
def multiple_exception_types():
    """Except clause catching multiple exception types."""
    return """
try:
    operation()
except (ValueError, KeyError, TypeError):
    handle_multiple()
"""
