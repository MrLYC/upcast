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
        "scan-django-views",
        "scan-django-models",
        "scan-signals",
        "scan-django-settings",
        "scan-queue-usage",
        "scan-offset-usage",
        "scan-redis-usage",
        "scan-module-symbols",
    ]:
        assert command in result.output


def test_main_help_does_not_reference_removed_django_report_command():
    """The CLI should not advertise the removed Django report merger."""
    runner = CliRunner()

    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "merge-django-report" not in result.output
