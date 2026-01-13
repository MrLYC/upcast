"""Tests for signal Pydantic models."""

import pytest

from upcast.models.signals import SignalInfo, SignalOutput, SignalSummary, SignalUsage


class TestSignalUsage:
    """Test SignalUsage model."""

    def test_basic_usage(self) -> None:
        """Test creating basic signal usage."""
        usage = SignalUsage(
            file="signals.py",
            lineno=10,
            handler="my_handler",
        )
        assert usage.file == "signals.py"
        assert usage.lineno == 10
        assert usage.handler == "my_handler"

    def test_usage_with_sender(self) -> None:
        """Test usage with sender."""
        usage = SignalUsage(
            file="models.py",
            lineno=20,
            sender="MyModel",
        )
        assert usage.sender == "MyModel"


class TestSignalInfo:
    """Test SignalInfo model."""

    def test_basic_info(self) -> None:
        """Test creating basic signal info."""
        info = SignalInfo(
            signal="post_save",
            type="django",
            category="model_signals",
            receivers=[],
            senders=[],
        )
        assert info.signal == "post_save"
        assert info.type == "django"

    def test_info_with_receivers(self) -> None:
        """Test signal info with receivers."""
        usage = SignalUsage(
            file="handlers.py",
            lineno=5,
            handler="on_save",
        )
        info = SignalInfo(
            signal="post_save",
            type="django",
            category="model_signals",
            receivers=[usage],
            senders=[],
        )
        assert len(info.receivers) == 1


class TestSignalSummary:
    """Test SignalSummary model."""

    def test_summary(self) -> None:
        """Test creating summary."""
        summary = SignalSummary(
            total_count=10,
            files_scanned=5,
            scan_duration_ms=100,
            django_receivers=5,
            django_senders=2,
            celery_receivers=3,
            celery_senders=1,
            custom_signals_defined=2,
            unused_custom_signals=0,
        )
        assert summary.django_receivers == 5
        assert summary.celery_receivers == 3


class TestSignalOutput:
    """Test SignalOutput model."""

    def test_output_structure(self) -> None:
        """Test output structure."""
        info = SignalInfo(
            signal="post_save",
            type="django",
            category="model_signals",
            receivers=[],
            senders=[],
        )
        summary = SignalSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=50,
            django_receivers=0,
            django_senders=0,
            celery_receivers=0,
            celery_senders=0,
            custom_signals_defined=0,
            unused_custom_signals=0,
        )
        output = SignalOutput(
            summary=summary,
            results=[info],
        )
        assert len(output.results) == 1
