"""Tests for log level detection in logging scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.logging_scanner import LoggingScanner


class TestStandardLogLevels:
    """Test detection of standard logging levels."""

    def test_debug_level(self, tmp_path):
        """Debug level should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.debug("Debug message")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].level == "debug"

    def test_info_level(self, tmp_path):
        """Info level should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.info("Info message")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].level == "info"

    def test_warning_level(self, tmp_path):
        """Warning level should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("Warning message")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].level == "warning"

    def test_error_level(self, tmp_path):
        """Error level should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Error message")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].level == "error"

    def test_critical_level(self, tmp_path):
        """Critical level should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.critical("Critical message")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].level == "critical"

    def test_exception_level(self, tmp_path):
        """Exception level should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            try:
                raise ValueError("Test")
            except:
                logger.exception("Exception message")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].level == "exception"


class TestMultipleLevels:
    """Test files with multiple log levels."""

    def test_mixed_levels(self, tmp_path):
        """Multiple log levels should all be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)

            logger.debug("Debug")
            logger.info("Info")
            logger.warning("Warning")
            logger.error("Error")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 4
        levels = {call.level for call in file_info.logging}
        assert levels == {"debug", "info", "warning", "error"}

    def test_level_summary(self, tmp_path):
        """Summary should count calls by level."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)

            logger.info("Info 1")
            logger.info("Info 2")
            logger.error("Error 1")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        assert output.summary.by_level["info"] == 2
        assert output.summary.by_level["error"] == 1


class TestLoguruLevels:
    """Test loguru log level detection."""

    def test_loguru_levels(self, tmp_path):
        """Loguru log levels should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from loguru import logger

            logger.debug("Debug")
            logger.info("Info")
            logger.warning("Warning")
            logger.error("Error")
            logger.critical("Critical")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.loguru) == 5
        levels = {call.level for call in file_info.loguru}
        assert "debug" in levels
        assert "info" in levels
        assert "error" in levels
