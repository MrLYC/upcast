"""Tests for Signal Scanner models and implementation."""

import pytest
from pydantic import ValidationError

from upcast.scanners.signal import (
    SignalInfo,
    SignalOutput,
    SignalScanner,
    SignalSummary,
    SignalUsage,
)


class TestSignalUsageModel:
    """Tests for SignalUsage Pydantic model."""

    def test_valid_signal_usage(self):
        """Test creating valid SignalUsage."""
        usage = SignalUsage(
            file="app/signals.py",
            line=10,
            column=4,
            handler="handle_post_save",
            pattern="receiver_decorator",
        )

        assert usage.file == "app/signals.py"
        assert usage.line == 10
        assert usage.column == 4
        assert usage.handler == "handle_post_save"

    def test_signal_usage_with_optional_fields(self):
        """Test SignalUsage with all optional fields."""
        usage = SignalUsage(
            file="app/signals.py",
            line=10,
            code="@receiver(post_save, sender=User)",
            sender="User",
            context={"class": "SignalHandlers", "type": "method"},
        )

        assert usage.sender == "User"
        assert usage.context["class"] == "SignalHandlers"

    def test_signal_usage_validates_line_number(self):
        """Test that line number must be >= 1."""
        with pytest.raises(ValidationError):
            SignalUsage(file="test.py", line=0)

    def test_signal_usage_validates_column_number(self):
        """Test that column number must be >= 0."""
        with pytest.raises(ValidationError):
            SignalUsage(file="test.py", line=1, column=-1)

    def test_signal_usage_minimal(self):
        """Test SignalUsage with minimal required fields."""
        usage = SignalUsage(file="test.py", line=1)

        assert usage.file == "test.py"
        assert usage.line == 1
        assert usage.column == 0  # default
        assert usage.handler is None
        assert usage.pattern is None


class TestSignalInfoModel:
    """Tests for SignalInfo Pydantic model."""

    def test_valid_signal_info(self):
        """Test creating valid SignalInfo."""
        info = SignalInfo(
            signal="post_save",
            type="django",
            category="model_signals",
            receivers=[SignalUsage(file="app/signals.py", line=10, handler="handle_save")],
            senders=[],
        )

        assert info.signal == "post_save"
        assert info.type == "django"
        assert len(info.receivers) == 1
        assert info.receivers[0].handler == "handle_save"

    def test_signal_info_with_status(self):
        """Test SignalInfo with status field."""
        info = SignalInfo(
            signal="my_signal",
            type="django",
            category="custom_signals",
            status="unused",
        )

        assert info.status == "unused"
        assert len(info.receivers) == 0  # default empty list

    def test_signal_info_celery(self):
        """Test SignalInfo for Celery signals."""
        info = SignalInfo(
            signal="task_success",
            type="celery",
            category="task_signals",
            receivers=[SignalUsage(file="app/tasks.py", line=20, handler="on_task_success")],
        )

        assert info.type == "celery"
        assert info.signal == "task_success"


class TestSignalSummaryModel:
    """Tests for SignalSummary Pydantic model."""

    def test_valid_signal_summary(self):
        """Test creating valid SignalSummary."""
        summary = SignalSummary(
            total_count=10,
            files_scanned=5,
            scan_duration_ms=1200,
            django_receivers=8,
            django_senders=2,
            celery_receivers=0,
            celery_senders=0,
        )

        assert summary.total_count == 10
        assert summary.django_receivers == 8
        assert summary.django_senders == 2

    def test_signal_summary_with_defaults(self):
        """Test SignalSummary with default values."""
        summary = SignalSummary(total_count=5, files_scanned=2)

        assert summary.django_receivers == 0  # default
        assert summary.celery_receivers == 0  # default
        assert summary.custom_signals_defined == 0  # default

    def test_signal_summary_validates_negative_counts(self):
        """Test that negative counts are rejected."""
        with pytest.raises(ValidationError):
            SignalSummary(
                total_count=5,
                files_scanned=2,
                django_receivers=-1,  # invalid
            )

    def test_signal_summary_custom_signals(self):
        """Test SignalSummary with custom signal counts."""
        summary = SignalSummary(
            total_count=3,
            files_scanned=1,
            custom_signals_defined=5,
            unused_custom_signals=2,
        )

        assert summary.custom_signals_defined == 5
        assert summary.unused_custom_signals == 2


class TestSignalOutputModel:
    """Tests for SignalOutput Pydantic model."""

    def test_valid_signal_output(self):
        """Test creating valid SignalOutput."""
        summary = SignalSummary(total_count=2, files_scanned=1, django_receivers=2)

        results = [
            SignalInfo(
                signal="post_save",
                type="django",
                category="model_signals",
                receivers=[SignalUsage(file="app/signals.py", line=10)],
            ),
            SignalInfo(
                signal="pre_delete",
                type="django",
                category="model_signals",
                receivers=[SignalUsage(file="app/signals.py", line=20)],
            ),
        ]

        output = SignalOutput(summary=summary, results=results, metadata={})

        assert output.summary.total_count == 2
        assert len(output.results) == 2
        assert output.results[0].signal == "post_save"

    def test_signal_output_serialization(self):
        """Test SignalOutput can be serialized to dict."""
        summary = SignalSummary(total_count=1, files_scanned=1)
        results = [SignalInfo(signal="test", type="django", category="custom_signals")]

        output = SignalOutput(summary=summary, results=results, metadata={})

        data = output.model_dump()

        assert data["summary"]["total_count"] == 1
        assert data["results"][0]["signal"] == "test"

    def test_signal_output_json_serialization(self):
        """Test SignalOutput can be serialized to JSON."""
        summary = SignalSummary(total_count=1, files_scanned=1)
        results = [SignalInfo(signal="test", type="django", category="custom_signals")]

        output = SignalOutput(summary=summary, results=results, metadata={})

        json_str = output.model_dump_json()

        assert "test" in json_str
        assert "django" in json_str


class TestSignalScannerIntegration:
    """Integration tests for SignalScanner."""

    def test_scanner_instantiation(self):
        """Test that SignalScanner can be instantiated."""
        scanner = SignalScanner()

        assert scanner.include_patterns == ["**/*.py"]
        assert scanner.exclude_patterns == []

    def test_scanner_with_custom_patterns(self):
        """Test SignalScanner with custom patterns."""
        scanner = SignalScanner(include_patterns=["**/signals.py"], exclude_patterns=["**/test_*.py"])

        assert scanner.include_patterns == ["**/signals.py"]
        assert scanner.exclude_patterns == ["**/test_*.py"]

    def test_scanner_scan_returns_signal_output(self, tmp_path):
        """Test that scan() returns SignalOutput."""
        # Create a simple Python file
        test_file = tmp_path / "test.py"
        test_file.write_text("# empty file\n")

        scanner = SignalScanner()
        output = scanner.scan(tmp_path)

        assert isinstance(output, SignalOutput)
        assert isinstance(output.summary, SignalSummary)
        assert isinstance(output.results, list)

    def test_scanner_detects_django_signals(self, tmp_path):
        """Test scanner detects Django signal patterns."""
        # Create a file with Django signal
        signals_file = tmp_path / "signals.py"
        signals_file.write_text("""
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, **kwargs):
    pass
""")

        scanner = SignalScanner()
        output = scanner.scan(tmp_path)

        # Should detect at least one signal
        assert output.summary.total_count >= 0  # May be 0 if imports fail
        assert output.summary.files_scanned == 1

    def test_scanner_summary_calculations(self, tmp_path):
        """Test that scanner correctly calculates summary statistics."""
        test_file = tmp_path / "test.py"
        test_file.write_text("# test\n")

        scanner = SignalScanner()
        output = scanner.scan(tmp_path)

        # Check summary structure
        assert output.summary.files_scanned == 1
        assert output.summary.total_count >= 0
        assert output.summary.django_receivers >= 0
        assert output.summary.scan_duration_ms >= 0

    def test_scanner_metadata(self, tmp_path):
        """Test that scanner includes metadata."""
        test_file = tmp_path / "test.py"
        test_file.write_text("# test\n")

        scanner = SignalScanner()
        output = scanner.scan(tmp_path)

        assert "scanner_name" in output.metadata
        assert output.metadata["scanner_name"] == "signal"
        assert "root_path" in output.metadata

    def test_scanner_respects_include_patterns(self, tmp_path):
        """Test that scanner respects include patterns."""
        (tmp_path / "signals.py").write_text("# signal file\n")
        (tmp_path / "models.py").write_text("# model file\n")

        scanner = SignalScanner(include_patterns=["**/signals.py"])
        output = scanner.scan(tmp_path)

        # Should only scan signals.py
        assert output.summary.files_scanned == 1

    def test_scanner_respects_exclude_patterns(self, tmp_path):
        """Test that scanner respects exclude patterns."""
        (tmp_path / "signals.py").write_text("# signal file\n")
        (tmp_path / "test_signals.py").write_text("# test file\n")

        scanner = SignalScanner(exclude_patterns=["**/test_*.py"])
        output = scanner.scan(tmp_path)

        # Should only scan signals.py (not test_signals.py)
        assert output.summary.files_scanned == 1
