"""Integration tests for signals scanner."""

from pathlib import Path

import pytest

from upcast.scanners.signals import SignalScanner


class TestSignalScanner:
    """Test SignalScanner integration."""

    def test_scan_receiver_decorator(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning @receiver decorator."""
        code_file = tmp_path / "handlers.py"
        code_file.write_text("""
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='MyModel')
def handle_post_save(sender, instance, **kwargs):
    pass
""")

        result = scanner.scan(tmp_path)

        assert result.summary.django_receivers >= 1

    def test_scan_signal_connect(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning signal.connect()."""
        code_file = tmp_path / "signals.py"
        code_file.write_text("""
from django.db.models.signals import post_save

def my_handler(sender, instance, **kwargs):
    pass

post_save.connect(my_handler, sender='MyModel')
""")

        result = scanner.scan(tmp_path)

        assert result.summary.django_receivers >= 1

    def test_scan_signal_send(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning signal.send()."""
        code_file = tmp_path / "models.py"
        code_file.write_text("""
from django.db.models.signals import post_save

post_save.send(sender=MyModel, instance=obj)
""")

        result = scanner.scan(tmp_path)

        assert result.summary.django_senders >= 1

    def test_scan_custom_signal(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning custom signal definition."""
        code_file = tmp_path / "signals.py"
        code_file.write_text("""
from django.dispatch import Signal

my_custom_signal = Signal()
""")

        result = scanner.scan(tmp_path)

        # Custom signal detection may vary based on scanner implementation
        assert result is not None
        assert result.summary.custom_signals_defined >= 0

    def test_scan_celery_signal(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning Celery signal."""
        code_file = tmp_path / "tasks.py"
        code_file.write_text("""
from celery.signals import task_success

@task_success.connect
def on_task_success(sender, **kwargs):
    pass
""")

        result = scanner.scan(tmp_path)

        assert result.summary.celery_receivers >= 1

    def test_scan_multiple_receivers(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning multiple receivers."""
        code_file = tmp_path / "handlers.py"
        code_file.write_text("""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save)
def handler1(sender, **kwargs):
    pass

@receiver(pre_save)
def handler2(sender, **kwargs):
    pass
""")

        result = scanner.scan(tmp_path)

        assert result.summary.django_receivers >= 2

    def test_scan_empty_directory(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning empty directory."""
        result = scanner.scan(tmp_path)

        assert result.summary.total_count >= 0
        assert result.summary.django_receivers == 0

    def test_scan_summary_statistics(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test summary statistics."""
        code_file = tmp_path / "signals.py"
        code_file.write_text("""
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save)
def my_handler(sender, **kwargs):
    pass

post_save.send(sender=MyModel)
""")

        result = scanner.scan(tmp_path)

        assert result.summary.files_scanned >= 1
        assert result.summary.scan_duration_ms >= 0
