"""Tests for logging scanner models."""

import pytest
from pydantic import ValidationError

from upcast.models.logging import LogCall, FileLoggingInfo, LoggingSummary, LoggingOutput


class TestLogCallModel:
    """Test LogCall model validation."""

    def test_log_call_valid(self):
        """Valid log call should be created successfully."""
        log_call = LogCall(
            logger_name="myapp.services",
            lineno=42,
            level="info",
            message="User logged in",
            args=["username"],
            type="string",
            block="function",
            sensitive_patterns=[],
        )

        assert log_call.logger_name == "myapp.services"
        assert log_call.lineno == 42
        assert log_call.level == "info"
        assert log_call.message == "User logged in"
        assert log_call.args == ["username"]
        assert log_call.type == "string"
        assert log_call.block == "function"
        assert log_call.sensitive_patterns == []

    def test_log_call_with_sensitive_patterns(self):
        """Log call with sensitive patterns should be created."""
        log_call = LogCall(
            logger_name="root",
            lineno=10,
            level="error",
            message="Failed auth",
            args=["password"],
            type="fstring",
            block="except",
            sensitive_patterns=["password"],
        )

        assert log_call.sensitive_patterns == ["password"]

    def test_log_call_invalid_lineno(self):
        """Log call with invalid line number should fail."""
        with pytest.raises(ValidationError):
            LogCall(
                logger_name="root",
                lineno=0,  # Must be >= 1
                level="info",
                message="Test",
                args=[],
                type="string",
                block="module",
            )

    def test_log_call_defaults(self):
        """Log call should have default values for optional fields."""
        log_call = LogCall(
            logger_name="root",
            lineno=1,
            level="debug",
            message="Test",
            type="string",
            block="module",
        )

        assert log_call.args == []
        assert log_call.sensitive_patterns == []


class TestFileLoggingInfoModel:
    """Test FileLoggingInfo model validation."""

    def test_file_logging_info_empty(self):
        """Empty FileLoggingInfo should be created."""
        info = FileLoggingInfo()

        assert info.logging == []
        assert info.loguru == []
        assert info.structlog == []
        assert info.django == []

    def test_file_logging_info_with_calls(self):
        """FileLoggingInfo with calls should be created."""
        log_call = LogCall(
            logger_name="root",
            lineno=1,
            level="info",
            message="Test",
            type="string",
            block="module",
        )

        info = FileLoggingInfo(logging=[log_call])

        assert len(info.logging) == 1
        assert info.logging[0] == log_call

    def test_file_logging_info_multiple_libraries(self):
        """FileLoggingInfo with multiple libraries should be created."""
        logging_call = LogCall(
            logger_name="root",
            lineno=1,
            level="info",
            message="Standard logging",
            type="string",
            block="module",
        )

        loguru_call = LogCall(
            logger_name="loguru",
            lineno=2,
            level="info",
            message="Loguru logging",
            type="string",
            block="module",
        )

        info = FileLoggingInfo(
            logging=[logging_call],
            loguru=[loguru_call],
        )

        assert len(info.logging) == 1
        assert len(info.loguru) == 1
        assert len(info.structlog) == 0
        assert len(info.django) == 0


class TestLoggingSummaryModel:
    """Test LoggingSummary model validation."""

    def test_logging_summary_valid(self):
        """Valid LoggingSummary should be created."""
        summary = LoggingSummary(
            total_count=10,
            total_log_calls=10,
            files_scanned=2,
            scan_duration_ms=500,
            by_library={"logging": 8, "loguru": 2},
            by_level={"info": 6, "error": 4},
            sensitive_calls=3,
        )

        assert summary.total_log_calls == 10
        assert summary.files_scanned == 2
        assert summary.by_library == {"logging": 8, "loguru": 2}
        assert summary.by_level == {"info": 6, "error": 4}
        assert summary.sensitive_calls == 3

    def test_logging_summary_defaults(self):
        """LoggingSummary should have default values."""
        summary = LoggingSummary(
            total_count=0,
            total_log_calls=0,
            files_scanned=0,
            scan_duration_ms=0,
            sensitive_calls=0,
        )

        assert summary.by_library == {}
        assert summary.by_level == {}
        assert summary.sensitive_calls == 0

    def test_logging_summary_invalid_negative(self):
        """LoggingSummary with negative values should fail."""
        with pytest.raises(ValidationError):
            LoggingSummary(
                total_count=0,
                total_log_calls=-1,  # Must be >= 0
                files_scanned=0,
                scan_duration_ms=0,
            )


class TestLoggingOutputModel:
    """Test LoggingOutput model validation."""

    def test_logging_output_valid(self):
        """Valid LoggingOutput should be created."""
        summary = LoggingSummary(
            total_count=1,
            total_log_calls=1,
            files_scanned=1,
            scan_duration_ms=100,
            sensitive_calls=0,
        )

        log_call = LogCall(
            logger_name="root",
            lineno=1,
            level="info",
            message="Test",
            type="string",
            block="module",
        )

        file_info = FileLoggingInfo(logging=[log_call])

        output = LoggingOutput(
            summary=summary,
            results={"test.py": file_info},
        )

        assert output.summary == summary
        assert len(output.results) == 1
        assert "test.py" in output.results

    def test_logging_output_empty(self):
        """Empty LoggingOutput should be created."""
        summary = LoggingSummary(
            total_count=0,
            total_log_calls=0,
            files_scanned=0,
            scan_duration_ms=0,
            sensitive_calls=0,
        )

        output = LoggingOutput(summary=summary, results={})

        assert len(output.results) == 0
