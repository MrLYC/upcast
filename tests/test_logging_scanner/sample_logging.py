"""Sample file with logging for testing."""

import logging

import structlog
from loguru import logger as loguru_logger

# Standard logging
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()


def test_standard_logging():
    """Test standard logging library."""
    logger.info("User logged in successfully")
    logger.warning("Password attempt failed for user %s", "admin")
    logger.error("API key {api_key} exposed in logs", extra={"api_key": "secret123"})
    logging.debug("Debug message")


def test_loguru():
    """Test loguru library."""
    loguru_logger.info("Application started")
    loguru_logger.error(f"Token {token} leaked", token="abc123")


def test_structlog():
    """Test structlog library."""
    struct_log = structlog.get_logger(__name__)
    struct_log.info("Processing request", user_id=123)
    struct_log.warning("Credit card number detected: {}", "4111-1111-1111-1111")


def test_fstring_logging():
    """Test f-string logging."""
    user = "john"
    logger.info(f"User {user} accessed resource")
    logger.error(f"Password hash: {hash('secret')}")
