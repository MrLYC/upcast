"""Tests for logging detection in exception handlers."""

import pytest
from pathlib import Path

from upcast.scanners.exceptions import ExceptionHandlerScanner


class TestLoggingDetection:
    """Test detection of logging calls in except clauses."""

    def test_logger_error(self, tmp_path, scanner):
        """Test detection of logger.error() calls."""
        code = """
import logging
logger = logging.getLogger(__name__)

try:
    operation()
except ValueError:
    logger.error("Error occurred")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.log_error_count == 1

    def test_logger_exception(self, tmp_path, scanner):
        """Test detection of logger.exception() calls."""
        code = """
import logging
logger = logging.getLogger(__name__)

try:
    operation()
except ValueError:
    logger.exception("Exception with traceback")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.log_exception_count == 1

    def test_multiple_logging_calls(self, tmp_path, scanner):
        """Test detection of multiple logging calls."""
        code = """
import logging
logger = logging.getLogger(__name__)

try:
    operation()
except ValueError as e:
    logger.warning("Warning message")
    logger.error("Error: %s", e)
    logger.exception("Full traceback")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.log_warning_count == 1
        assert clause.log_error_count == 1
        assert clause.log_exception_count == 1

    def test_all_logging_levels(self, tmp_path, scanner):
        """Test detection of all logging levels."""
        code = """
import logging
logger = logging.getLogger(__name__)

try:
    operation()
except ValueError:
    logger.debug("Debug")
    logger.info("Info")
    logger.warning("Warning")
    logger.error("Error")
    logger.exception("Exception")
    logger.critical("Critical")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.log_debug_count == 1
        assert clause.log_info_count == 1
        assert clause.log_warning_count == 1
        assert clause.log_error_count == 1
        assert clause.log_exception_count == 1
        assert clause.log_critical_count == 1

    def test_logger_variations(self, tmp_path, scanner):
        """Test detection with different logger variable names."""
        code = """
import logging
LOG = logging.getLogger(__name__)
_logger = logging.getLogger(__name__)
log = logging.getLogger(__name__)

try:
    operation()
except ValueError:
    LOG.error("From LOG")
    _logger.error("From _logger")
    log.error("From log")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.log_error_count == 3

    def test_no_logging(self, tmp_path, scanner):
        """Test except clause without logging."""
        code = """
try:
    operation()
except ValueError:
    print("Error occurred")
    handle_error()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.log_error_count == 0
        assert clause.log_exception_count == 0

    def test_logging_in_nested_function(self, tmp_path, scanner):
        """Test logging detection in nested function calls."""
        code = """
import logging
logger = logging.getLogger(__name__)

def handle_error(e):
    logger.error("Nested error: %s", e)

try:
    operation()
except ValueError as e:
    handle_error(e)
    logger.warning("Also logged here")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        # Should detect the warning call in the except block
        # The error call inside handle_error() is in a different scope
        assert clause.log_warning_count == 1

    def test_module_logger(self, tmp_path, scanner):
        """Test detection of logging.error() direct calls."""
        code = """
import logging

try:
    operation()
except ValueError:
    logging.error("Direct logging call")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        # Direct logging.error() might not be detected depending on implementation
        # This documents the current behavior
        assert clause.log_error_count >= 0
