"""Cross-scanner output-contract tests."""

from pathlib import Path

import pytest

from upcast.scanners import (
    BlockingOperationsScanner,
    ComplexityScanner,
    ConcurrencyScanner,
    DjangoModelScanner,
    DjangoSettingsScanner,
    DjangoUrlScanner,
    DjangoViewScanner,
    EnvVarScanner,
    ExceptionHandlerScanner,
    HttpRequestsScanner,
    LoggingScanner,
    MetricsScanner,
    ModuleSymbolScanner,
    OffsetUsageScanner,
    QueueUsageScanner,
    RedisUsageScanner,
    SignalScanner,
    UnitTestScanner,
)


SCANNERS = [
    pytest.param(BlockingOperationsScanner(), id="blocking-operations"),
    pytest.param(ComplexityScanner(), id="complexity-patterns"),
    pytest.param(ConcurrencyScanner(), id="concurrency-patterns"),
    pytest.param(DjangoModelScanner(), id="django-models"),
    pytest.param(DjangoSettingsScanner(), id="django-settings"),
    pytest.param(DjangoUrlScanner(), id="django-urls"),
    pytest.param(DjangoViewScanner(), id="django-views"),
    pytest.param(EnvVarScanner(), id="env-vars"),
    pytest.param(ExceptionHandlerScanner(), id="exception-handlers"),
    pytest.param(HttpRequestsScanner(), id="http-requests"),
    pytest.param(LoggingScanner(), id="logging"),
    pytest.param(MetricsScanner(), id="metrics"),
    pytest.param(ModuleSymbolScanner(), id="module-symbols"),
    pytest.param(OffsetUsageScanner(), id="offset-usage"),
    pytest.param(QueueUsageScanner(), id="queue-usage"),
    pytest.param(RedisUsageScanner(), id="redis-usage"),
    pytest.param(SignalScanner(), id="signals"),
    pytest.param(UnitTestScanner(), id="unit-tests"),
]


@pytest.fixture
def eligible_source_files(tmp_path: Path) -> Path:
    """Provide ordinary eligible files that intentionally contain no scanner findings."""
    (tmp_path / "module.py").write_text("value = 1\n", encoding="utf-8")
    (tmp_path / "models.py").write_text("value = 2\n", encoding="utf-8")
    (tmp_path / "urls.py").write_text("urlpatterns = []\n", encoding="utf-8")
    (tmp_path / "test_module.py").write_text("value = 3\n", encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize("scanner", SCANNERS)
def test_summary_files_scanned_counts_all_eligible_files(
    eligible_source_files: Path,
    scanner,
) -> None:
    """A no-finding scan must still report every file it parsed."""
    eligible_files = scanner.get_files_to_scan(eligible_source_files)

    output = scanner.scan(eligible_source_files)

    assert output.summary.files_scanned == len(eligible_files)
