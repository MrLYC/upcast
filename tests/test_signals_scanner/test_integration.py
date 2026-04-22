"""Integration tests for signals scanner."""

from pathlib import Path

from upcast.models.signals import SignalInfo, SignalOutput
from upcast.scanners.signals import SignalScanner


class TestSignalScanner:
    """Test SignalScanner integration."""

    @staticmethod
    def _get_signal(result: SignalOutput, signal_name: str) -> SignalInfo:
        """Get a signal entry by name from scanner output."""
        return next(signal for signal in result.results if signal.signal == signal_name)

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
        signal = self._get_signal(result, "post_save")
        assert len(signal.senders) == 1
        assert signal.senders[0].sender == "MyModel"

    def test_scan_signal_send_robust_includes_sender(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning signal.send_robust() with sender."""
        code_file = tmp_path / "models.py"
        code_file.write_text("""
from django.db.models.signals import post_save

post_save.send_robust(sender=MyModel, instance=obj)
""")

        result = scanner.scan(tmp_path)

        assert result.summary.django_senders >= 1
        signal = self._get_signal(result, "post_save")
        assert len(signal.senders) == 1
        assert signal.senders[0].sender == "MyModel"

    def test_scan_custom_signal(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test scanning custom signal definition."""
        code_file = tmp_path / "signals.py"
        code_file.write_text("""
from django.dispatch import Signal

my_custom_signal = Signal(providing_args=["user"])
""")

        result = scanner.scan(tmp_path)

        assert result.summary.custom_signals_defined == 1
        signal = self._get_signal(result, "my_custom_signal")
        assert signal.category == "custom_signals"
        assert signal.definition is not None
        assert signal.definition.file == "signals.py"
        assert signal.definition.lineno >= 1
        assert signal.definition.providing_args == ["user"]

    def test_scan_non_signal_send_is_ignored(self, tmp_path: Path, scanner: SignalScanner) -> None:
        """Test arbitrary .send() calls are not treated as signal sends."""
        code_file = tmp_path / "mailer.py"
        code_file.write_text("""
class Mailer:
    def send(self, sender, instance):
        pass


mail = Mailer()
mail.send(sender=User, instance=obj)
""")

        result = scanner.scan(tmp_path)

        assert result.summary.django_senders == 0
        assert result.summary.celery_senders == 0
        assert all(signal.signal != "mail" for signal in result.results)

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
