"""Tests for edge cases in logging scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.logging_scanner import LoggingScanner


class TestInvalidSyntax:
    """Test handling of invalid Python syntax."""

    def test_invalid_syntax_skipped(self, tmp_path):
        """Files with invalid syntax should be skipped gracefully."""
        test_file = tmp_path / "test_invalid.py"
        test_file.write_text("def broken(:\n    logger.info('test')\n")

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        # Should not crash, just return empty results
        assert output.summary.total_log_calls == 0


class TestEmptyAndMinimalFiles:
    """Test empty and minimal files."""

    def test_empty_file(self, tmp_path):
        """Empty file should return no results."""
        test_file = tmp_path / "test_empty.py"
        test_file.write_text("")

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_log_calls == 0
        assert len(output.results) == 0

    def test_file_with_only_imports(self, tmp_path):
        """File with only imports should return no results."""
        test_file = tmp_path / "test_imports.py"
        test_file.write_text(
            dedent("""
            import logging
            from loguru import logger
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_log_calls == 0

    def test_file_with_logger_but_no_calls(self, tmp_path):
        """File with logger creation but no calls should return no results."""
        test_file = tmp_path / "test_no_calls.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            
            def foo():
                pass
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_log_calls == 0


class TestNonLoggingMethodCalls:
    """Test that non-logging method calls are not detected."""

    def test_non_logger_info_method(self, tmp_path):
        """info() method on non-logger should not be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class MyClass:
                def info(self, msg):
                    print(msg)
            
            obj = MyClass()
            obj.info("Not a log call")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_log_calls == 0

    def test_function_named_logger(self, tmp_path):
        """Function named 'logger' should not be detected as logging."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def logger():
                return "Not a logger"
            
            # This is a function call, not a logger creation
            result = logger()
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_log_calls == 0


class TestComplexLogMessages:
    """Test complex log message scenarios."""

    def test_multiline_message(self, tmp_path):
        """Multiline message should be captured."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info('''This is a
            multiline
            message''')
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        # Message should be captured (might be on one line)
        assert "multiline" in file_info.logging[0].message

    def test_log_with_no_message(self, tmp_path):
        """Log call without arguments should be handled."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            
            # This shouldn't crash the scanner
            try:
                logger.info()
            except:
                pass
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)

        # Should not detect this as a valid log call
        assert output.summary.total_log_calls == 0

    def test_log_with_complex_expression(self, tmp_path):
        """Log call with complex message expression should be handled."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            
            def get_message():
                return "Dynamic message"
            
            logger.info(get_message())
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 1
        # Should capture the expression as string
        assert file_info.logging[0].message


class TestDirectoryScanning:
    """Test scanning directories."""

    def test_scan_directory_with_multiple_files(self, tmp_path):
        """Scanning directory should process all Python files."""
        (tmp_path / "file1.py").write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.info("File 1")
        """)
        )

        (tmp_path / "file2.py").write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            logger.info("File 2")
        """)
        )

        (tmp_path / "ignored.txt").write_text("Not a Python file")

        scanner = LoggingScanner()
        output = scanner.scan(tmp_path)

        assert output.summary.files_scanned == 2
        assert output.summary.total_log_calls == 2

    def test_scan_nested_directories(self, tmp_path):
        """Scanning should recurse into subdirectories."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        (tmp_path / "root.py").write_text(
            dedent("""
            import logging
            logging.info("Root")
        """)
        )

        (subdir / "nested.py").write_text(
            dedent("""
            import logging
            logging.info("Nested")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(tmp_path)

        assert output.summary.files_scanned == 2
        assert output.summary.total_log_calls == 2


class TestPatternFiltering:
    """Test file pattern filtering."""

    def test_exclude_patterns(self, tmp_path):
        """Files matching exclude patterns should be skipped."""
        (tmp_path / "include.py").write_text(
            dedent("""
            import logging
            logging.info("Include")
        """)
        )

        (tmp_path / "exclude.py").write_text(
            dedent("""
            import logging
            logging.info("Exclude")
        """)
        )

        scanner = LoggingScanner(exclude_patterns=["**/exclude.py"])
        output = scanner.scan(tmp_path)

        assert output.summary.files_scanned == 1
        assert "exclude.py" not in output.results

    def test_include_patterns(self, tmp_path):
        """Only files matching include patterns should be processed."""
        (tmp_path / "match.py").write_text(
            dedent("""
            import logging
            logging.info("Match")
        """)
        )

        (tmp_path / "nomatch.py").write_text(
            dedent("""
            import logging
            logging.info("No match")
        """)
        )

        scanner = LoggingScanner(include_patterns=["**/match.py"])
        output = scanner.scan(tmp_path)

        assert output.summary.files_scanned == 1
        assert "match.py" in str(output.results.keys())


class TestLineNumbers:
    """Test line number tracking."""

    def test_line_numbers_tracked(self, tmp_path):
        """Line numbers should be accurately tracked."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info("Line 5")
            logger.info("Line 6")
            
            
            logger.info("Line 9")
        """)
        )

        scanner = LoggingScanner()
        output = scanner.scan(test_file)
        file_info = list(output.results.values())[0]

        assert len(file_info.logging) == 3
        line_numbers = [call.lineno for call in file_info.logging]
        assert 5 in line_numbers
        assert 6 in line_numbers
        assert 9 in line_numbers
