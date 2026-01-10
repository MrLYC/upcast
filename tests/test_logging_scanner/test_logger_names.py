"""Tests for logger name resolution in logging scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.logging_scanner import LoggingScanner


class TestLoggerNameResolution:
    """Test logger name resolution."""

    def test_getlogger_with_name(self, tmp_path):
        """Logger with __name__ should resolve to module path."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.info("Test")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        # Should resolve to module name (test)
        assert "test" in file_info.logging[0].logger_name

    def test_getlogger_with_string(self, tmp_path):
        """Logger with string name should use that name."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger("myapp.services")
            logger.info("Test")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].logger_name == "myapp.services"

    def test_getlogger_no_args(self, tmp_path):
        """Logger without arguments should be root logger."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger()
            logger.info("Test")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].logger_name == "root"

    def test_module_level_logging(self, tmp_path):
        """Module-level logging should use root logger."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logging.info("Test")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        assert file_info.logging[0].logger_name == "root"


class TestLoguruLoggerName:
    """Test loguru logger name resolution."""

    def test_loguru_direct_import(self, tmp_path):
        """Loguru logger should have 'loguru' as name."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from loguru import logger
            logger.info("Test")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.loguru) == 1
        assert file_info.loguru[0].logger_name == "loguru"


class TestStructlogLoggerName:
    """Test structlog logger name resolution."""

    def test_structlog_get_logger(self, tmp_path):
        """Structlog logger should use module path."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import structlog
            logger = structlog.get_logger()
            logger.info("Test")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.structlog) == 1
        # Should use module path
        assert "test" in file_info.structlog[0].logger_name

    def test_structlog_with_name(self, tmp_path):
        """Structlog logger with name should use that name."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import structlog
            logger = structlog.get_logger("myapp")
            logger.info("Test")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.structlog) == 1
        assert file_info.structlog[0].logger_name == "myapp"


class TestMultipleLoggers:
    """Test files with multiple logger instances."""

    def test_multiple_loggers_same_file(self, tmp_path):
        """Multiple loggers in same file should be tracked separately."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            
            logger1 = logging.getLogger("app.service1")
            logger2 = logging.getLogger("app.service2")
            
            logger1.info("From service1")
            logger2.info("From service2")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 2
        logger_names = {call.logger_name for call in file_info.logging}
        assert "app.service1" in logger_names
        assert "app.service2" in logger_names
