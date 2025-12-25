"""Tests for LoggingScanner."""

from pathlib import Path

import pytest

from upcast.scanners.logging_scanner import LoggingScanner


@pytest.fixture
def sample_file():
    """Get path to sample file."""
    return Path(__file__).parent / "sample_logging.py"


@pytest.fixture
def scanner():
    """Create scanner instance."""
    return LoggingScanner(verbose=False, check_sensitive=True)


def test_scan_file_detects_logging(scanner, sample_file):
    """Test that scanner detects logging calls."""
    output = scanner.scan(sample_file)

    # Check summary
    assert output.summary.total_log_calls > 0
    assert output.summary.files_scanned == 1

    # Check results
    assert len(output.results) == 1
    file_info = next(iter(output.results.values()))

    # Should detect standard logging
    assert len(file_info.logging) > 0

    # Should detect loguru
    assert len(file_info.loguru) > 0

    # Should detect structlog
    assert len(file_info.structlog) > 0


def test_detects_logger_names(scanner, sample_file):
    """Test that logger names are correctly resolved."""
    output = scanner.scan(sample_file)
    file_info = next(iter(output.results.values()))

    # Check logger names in standard logging
    logger_names = {call.logger_name for call in file_info.logging}
    assert "test_logging_scanner.sample_logging" in logger_names or "sample_logging" in logger_names
    assert "root" in logger_names

    # Check loguru logger name
    loguru_names = {call.logger_name for call in file_info.loguru}
    assert "loguru" in loguru_names


def test_detects_log_levels(scanner, sample_file):
    """Test that log levels are detected."""
    output = scanner.scan(sample_file)
    file_info = next(iter(output.results.values()))

    # Collect all log levels
    all_calls = file_info.logging + file_info.loguru + file_info.structlog + file_info.django
    levels = {call.level for call in all_calls}

    # Should detect multiple levels
    assert "info" in levels
    assert "warning" in levels or "error" in levels


def test_detects_message_types(scanner, sample_file):
    """Test that message format types are detected."""
    output = scanner.scan(sample_file)
    file_info = next(iter(output.results.values()))

    # Collect all message types
    all_calls = file_info.logging + file_info.loguru + file_info.structlog + file_info.django
    types = {call.type for call in all_calls}

    # Should detect different format types
    assert "string" in types
    assert "fstring" in types or "percent" in types


def test_detects_sensitive_data(scanner, sample_file):
    """Test that sensitive data is detected."""
    output = scanner.scan(sample_file)
    file_info = next(iter(output.results.values()))

    # Collect all calls
    all_calls = file_info.logging + file_info.loguru + file_info.structlog + file_info.django

    # Should detect calls with sensitive data
    sensitive_calls = [call for call in all_calls if call.sensitive_patterns]
    assert len(sensitive_calls) > 0

    # Check sensitive patterns
    all_patterns = []
    for call in sensitive_calls:
        all_patterns.extend(call.sensitive_patterns)

    # Should detect common sensitive keywords
    assert any(pattern in ["password", "token", "api_key", "credit_card"] for pattern in all_patterns)


def test_summary_statistics(scanner, sample_file):
    """Test that summary statistics are correct."""
    output = scanner.scan(sample_file)

    # Check by_library counts
    assert "logging" in output.summary.by_library
    assert output.summary.by_library["logging"] > 0

    # Check by_level counts
    assert len(output.summary.by_level) > 0

    # Check sensitive calls count
    assert output.summary.sensitive_calls >= 0


def test_empty_file(scanner, tmp_path):
    """Test scanning empty file."""
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("# Empty file\n")

    output = scanner.scan(empty_file)

    # Should return no results
    assert output.summary.total_log_calls == 0
    assert len(output.results) == 0


def test_file_without_logging(scanner, tmp_path):
    """Test scanning file without logging."""
    no_logging = tmp_path / "no_logging.py"
    no_logging.write_text(
        """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
"""
    )

    output = scanner.scan(no_logging)

    # Should return no results
    assert output.summary.total_log_calls == 0
    assert len(output.results) == 0


def test_sensitive_check_disabled(sample_file):
    """Test scanning with sensitive check disabled."""
    scanner = LoggingScanner(verbose=False, check_sensitive=False)
    output = scanner.scan(sample_file)

    file_info = next(iter(output.results.values()))
    all_calls = file_info.logging + file_info.loguru + file_info.structlog + file_info.django

    # No calls should be marked as sensitive
    assert all(not call.sensitive_patterns for call in all_calls)
    assert output.summary.sensitive_calls == 0


def test_scan_directory(scanner, sample_file):
    """Test scanning directory."""
    directory = sample_file.parent
    output = scanner.scan(directory)

    # Should find at least the sample file
    assert output.summary.total_log_calls > 0
    assert output.summary.files_scanned >= 1


def test_message_extraction(scanner, tmp_path):
    """Test message extraction from different formats."""
    test_file = tmp_path / "test_messages.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)

def test():
    # String literal
    logger.info("Simple message")

    # Percent formatting
    logger.info("User %s logged in", "john")

    # F-string
    user = "jane"
    logger.info(f"Welcome {user}")

    # Format method
    logger.info("Count: {}".format(42))
"""
    )

    output = scanner.scan(test_file)
    file_info = next(iter(output.results.values()))

    messages = [call.message for call in file_info.logging]

    # Check that messages are extracted
    assert len(messages) > 0
    assert any("Simple message" in msg for msg in messages)


def test_argument_extraction(scanner, tmp_path):
    """Test argument extraction from log calls."""
    test_file = tmp_path / "test_args.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)

def test():
    logger.info("User: %s, ID: %d", username, user_id)
    logger.error("Error occurred", exc_info=True, extra={"context": "value"})
"""
    )

    output = scanner.scan(test_file)
    file_info = next(iter(output.results.values()))

    # Check that arguments are extracted
    assert len(file_info.logging) > 0

    # At least one call should have arguments
    assert any(len(call.args) > 0 for call in file_info.logging)


def test_variable_message_inference(scanner, tmp_path):
    """Test that messages passed as variables are inferred when possible."""
    test_file = tmp_path / "test_variable.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)

# Module-level constant
MSG_SUCCESS = "Operation completed"

def test():
    # Should infer from module-level constant
    logger.info(MSG_SUCCESS)

    # Should infer from local variable
    msg = "User action"
    logger.info(msg)

    # Cannot infer from parameter
    def log_it(message):
        logger.info(message)
"""
    )

    output = scanner.scan(test_file)
    file_info = next(iter(output.results.values()))

    messages = [call.message for call in file_info.logging]

    # Should have inferred messages
    assert "Operation completed" in messages
    assert "User action" in messages

    # Should have variable name with backticks for non-inferable
    assert any("`message`" in msg for msg in messages)


def test_fstring_template_extraction(scanner, tmp_path):
    """Test that f-string messages are extracted without f'' wrapper."""
    test_file = tmp_path / "test_fstring.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)

def test():
    user = "john"
    logger.info(f"Welcome {user}")
    logger.error(f"Error in {module} at line {lineno}")
"""
    )

    output = scanner.scan(test_file)
    file_info = next(iter(output.results.values()))

    messages = [call.message for call in file_info.logging]

    # Should not contain f'' wrapper
    assert not any(msg.startswith("f'") or msg.startswith('f"') for msg in messages)

    # Should contain placeholder format
    assert any("{user}" in msg for msg in messages)
    assert any("{module}" in msg and "{lineno}" in msg for msg in messages)


def test_block_type_detection(scanner, tmp_path):
    """Test that block types are detected correctly."""
    test_file = tmp_path / "test_blocks.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)

# Module level
logger.info("Module level")

class MyClass:
    def method(self):
        # Function level
        logger.info("In method")

        # If block
        if True:
            logger.info("In if")
        else:
            logger.info("In else")

        # For loop
        for i in range(10):
            logger.info("In for")

        # While loop
        while False:
            logger.info("In while")

        # Try-except-finally
        try:
            logger.info("In try")
        except Exception:
            logger.error("In except")
        finally:
            logger.info("In finally")

        # With statement
        with open("test.txt", "w") as f:
            logger.info("In with")
"""
    )

    output = scanner.scan(test_file)
    file_info = next(iter(output.results.values()))

    blocks = [call.block for call in file_info.logging]

    # Should detect all block types
    assert "module" in blocks
    assert "function" in blocks
    assert "if" in blocks
    assert "else" in blocks
    assert "for" in blocks
    assert "try" in blocks
    assert "except" in blocks
    assert "finally" in blocks
    assert "with" in blocks


def test_custom_sensitive_keywords(tmp_path):
    """Test that custom sensitive keywords can be provided."""
    test_file = tmp_path / "test_custom_sensitive.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)

def test():
    # Default sensitive keyword
    logger.info("User password: %s", user_password)

    # Custom sensitive keyword
    logger.info("API endpoint: %s", api_endpoint)

    # Another custom keyword
    logger.info("Database connection: %s", db_connection)

    # Non-sensitive
    logger.info("User name: %s", user_name)
"""
    )

    # Test with default keywords (should only detect 'password')
    scanner_default = LoggingScanner(verbose=False, check_sensitive=True)
    output_default = scanner_default.scan(test_file)
    file_info_default = next(iter(output_default.results.values()))
    sensitive_calls_default = [call for call in file_info_default.logging if call.sensitive_patterns]
    assert len(sensitive_calls_default) == 1
    assert any("password" in pattern.lower() for call in sensitive_calls_default for pattern in call.sensitive_patterns)

    # Test with custom keywords (should detect 'api_endpoint' and 'db_connection')
    scanner_custom = LoggingScanner(
        verbose=False, check_sensitive=True, sensitive_keywords=["api_endpoint", "db_connection", "database"]
    )
    output_custom = scanner_custom.scan(test_file)
    file_info_custom = next(iter(output_custom.results.values()))
    sensitive_calls_custom = [call for call in file_info_custom.logging if call.sensitive_patterns]

    # Should detect api_endpoint and db_connection (not password)
    assert len(sensitive_calls_custom) == 2
    patterns_found = [pattern for call in sensitive_calls_custom for pattern in call.sensitive_patterns]
    assert "api_endpoint" in patterns_found or "db_connection" in patterns_found


def test_default_sensitive_keywords_used_when_none_provided():
    """Test that default sensitive keywords are used when none are provided."""
    scanner = LoggingScanner(verbose=False, check_sensitive=True, sensitive_keywords=None)

    # Should use default keywords
    assert scanner.sensitive_keywords == LoggingScanner.DEFAULT_SENSITIVE_KEYWORDS
    assert "password" in scanner.sensitive_keywords
    assert "token" in scanner.sensitive_keywords
    assert "api_key" in scanner.sensitive_keywords


def test_sensitive_keyword_matching_with_word_boundaries(tmp_path):
    """Test that sensitive keyword matching uses word boundaries to avoid false positives."""
    test_file = tmp_path / "test_word_boundaries.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)

def test():
    # Should NOT match: "key" in "keyboard_input"
    logger.info("Input received: %s", keyboard_input)

    # Should match: "key" as complete word in "api_key"
    logger.info("Value: %s", api_key)

    # Should NOT match: "pass" in "bypass_mode"
    logger.info("Mode enabled: %s", bypass_mode)

    # Should match: "password" as complete word in "user_password"
    logger.info("Value: %s", user_password)
"""
    )

    # Test with "key" and "password" as keywords
    scanner = LoggingScanner(verbose=False, check_sensitive=True, sensitive_keywords=["key", "password"])
    output = scanner.scan(test_file)
    file_info = next(iter(output.results.values()))

    # Check each call individually
    calls = file_info.logging
    assert len(calls) == 4

    # First call: keyboard_input should NOT be sensitive (key is inside keyboard)
    assert not calls[0].sensitive_patterns
    assert "keyboard_input" not in calls[0].sensitive_patterns

    # Second call: api_key should be sensitive (contains "key" as word)
    assert calls[1].sensitive_patterns
    assert "api_key" in calls[1].sensitive_patterns

    # Third call: bypass_mode should NOT be sensitive (pass is inside bypass)
    assert not calls[2].sensitive_patterns
    assert "bypass_mode" not in calls[2].sensitive_patterns

    # Fourth call: user_password should be sensitive (contains "password" as word)
    assert calls[3].sensitive_patterns
    assert "user_password" in calls[3].sensitive_patterns
