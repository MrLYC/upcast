"""Integration tests for signal scanner."""

from pathlib import Path

from upcast.signal_scanner.checker import SignalChecker

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_scan_django_signals():
    """Test scanning Django signal patterns."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "django_signals.py"))

    results = checker.get_results()

    assert "django" in results
    django_signals = results["django"]

    # Check model signals
    assert "model_signals" in django_signals
    assert "post_save" in django_signals["model_signals"]
    assert "pre_delete" in django_signals["model_signals"]
    assert "post_delete" in django_signals["model_signals"]

    # Check request signals
    assert "request_signals" in django_signals
    assert "request_started" in django_signals["request_signals"]
    assert "request_finished" in django_signals["request_signals"]


def test_scan_celery_signals():
    """Test scanning Celery signal patterns."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "celery_signals.py"))

    results = checker.get_results()

    assert "celery" in results
    celery_signals = results["celery"]

    # Check task signals
    assert "task_signals" in celery_signals
    assert "task_prerun" in celery_signals["task_signals"]
    assert "task_postrun" in celery_signals["task_signals"]
    assert "task_failure" in celery_signals["task_signals"]
    assert "task_retry" in celery_signals["task_signals"]

    # Check worker signals
    assert "worker_signals" in celery_signals
    assert "worker_ready" in celery_signals["worker_signals"]
    assert "worker_shutdown" in celery_signals["worker_signals"]


def test_scan_custom_signals():
    """Test scanning custom signal definitions."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR), verbose=True)
    checker.check_file(str(FIXTURES_DIR / "custom_signals.py"))

    results = checker.get_results()

    assert "django" in results
    django_signals = results["django"]

    # Check custom signals with handlers
    assert "custom_signals" in django_signals
    assert "order_paid" in django_signals["custom_signals"]
    assert "payment_failed" in django_signals["custom_signals"]
    assert "shipment_dispatched" in django_signals["custom_signals"]

    # Check unused custom signal is detected in verbose mode
    if "unused_custom_signals" in django_signals:
        unused = django_signals["unused_custom_signals"]
        assert any(s["name"] == "user_deactivated" for s in unused)


def test_scan_mixed_signals():
    """Test scanning file with both Django and Celery signals."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "mixed_signals.py"))

    results = checker.get_results()

    # Should have both frameworks
    assert "django" in results
    assert "celery" in results

    # Check Django signals
    assert "model_signals" in results["django"]
    assert "post_save" in results["django"]["model_signals"]

    # Check Celery signals
    assert "task_signals" in results["celery"]
    assert "task_postrun" in results["celery"]["task_signals"]
    assert "task_failure" in results["celery"]["task_signals"]


def test_handler_context_extraction():
    """Test that handler context is extracted correctly."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "django_signals.py"))

    results = checker.get_results()
    django_signals = results["django"]

    # Check module-level function
    signal_data = django_signals["model_signals"]["post_save"]
    receivers = signal_data["receivers"]
    module_handler = next(h for h in receivers if h["handler"] == "order_created")
    assert "context" in module_handler
    assert module_handler["context"]["type"] == "function"

    # Check method in class
    signal_data = django_signals["model_signals"]["pre_save"]
    receivers = signal_data["receivers"]
    method_handler = next(h for h in receivers if h["handler"] == "on_user_save")
    assert "context" in method_handler
    assert method_handler["context"]["type"] == "method"
    assert method_handler["context"]["class"] == "SignalHandlers"


def test_signal_aggregation():
    """Test that handlers are aggregated by signal name."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "django_signals.py"))

    results = checker.get_results()
    django_signals = results["django"]

    # post_save should have multiple handlers
    post_save_data = django_signals["model_signals"]["post_save"]
    post_save_receivers = post_save_data["receivers"]
    assert len(post_save_receivers) >= 2  # order_created + save_handler


def test_sender_extraction():
    """Test that sender information is extracted."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "django_signals.py"))

    results = checker.get_results()
    django_signals = results["django"]

    # Check handler with sender
    signal_data = django_signals["model_signals"]["post_save"]
    receivers = signal_data["receivers"]
    handler_with_sender = next(h for h in receivers if h["handler"] == "order_created")
    assert "sender" in handler_with_sender
    assert handler_with_sender["sender"] == "Order"


def test_summary_statistics():
    """Test summary statistics generation."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "django_signals.py"))
    checker.check_file(str(FIXTURES_DIR / "celery_signals.py"))

    summary = checker.get_summary()

    assert "django_receivers" in summary
    assert summary["django_receivers"] > 0

    assert "celery_receivers" in summary
    assert summary["celery_receivers"] > 0


def test_empty_file():
    """Test scanning empty file doesn't crash."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))

    # Create empty temp file
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# Empty file\n")
        temp_file = f.name

    try:
        checker.check_file(temp_file)
        results = checker.get_results()
        assert results == {}
    finally:
        Path(temp_file).unlink()


def test_import_tracking():
    """Test that signal imports are tracked."""
    checker = SignalChecker(root_path=str(FIXTURES_DIR))
    checker.check_file(str(FIXTURES_DIR / "django_signals.py"))

    # Check Django imports are tracked
    assert len(checker.django_imports) > 0
    assert "receiver" in checker.django_imports or "post_save" in checker.django_imports

    # Check custom signals are tracked
    checker2 = SignalChecker(root_path=str(FIXTURES_DIR))
    checker2.check_file(str(FIXTURES_DIR / "custom_signals.py"))
    assert len(checker2.custom_signals) > 0
