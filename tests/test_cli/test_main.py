"""Functional tests for the public main CLI."""

from click.testing import CliRunner

from upcast.main import main


def test_main_help_lists_all_public_commands():
    """The public CLI help should expose all supported scan commands."""
    runner = CliRunner()

    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    for command in [
        "scan-complexity-patterns",
        "scan-env-vars",
        "scan-blocking-operations",
        "scan-http-requests",
        "scan-metrics",
        "scan-logging",
        "scan-concurrency-patterns",
        "scan-exception-handlers",
        "scan-unit-tests",
        "scan-django-urls",
        "scan-django-models",
        "scan-signals",
        "scan-django-settings",
        "scan-redis-usage",
        "scan-module-symbols",
    ]:
        assert command in result.output
