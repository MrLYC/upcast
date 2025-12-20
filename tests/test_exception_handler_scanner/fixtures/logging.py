# ruff: noqa
"""Various logging patterns in exception handlers."""

import logging

logger = logging.getLogger(__name__)
LOG = logging.getLogger(__name__)


def error_logging():
    """Exception handler with error logging."""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        logger.error("Division by zero")


def exception_logging():
    """Exception handler with exception logging (includes traceback)."""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero with traceback")


def multiple_log_levels():
    """Exception handler with multiple log levels."""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")


def different_logger_names():
    """Test different logger variable names."""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        LOG.error("Using LOG variable")


def no_logging():
    """Exception handler without logging."""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        print("Error occurred")
