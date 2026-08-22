"""Contract tests for queue usage output models."""

import pytest


def _models():
    try:
        from upcast.models.queue_usage import (
            QueueParameter,
            QueueUsage,
            QueueUsageOutput,
            QueueUsageSummary,
        )
    except ModuleNotFoundError as exc:
        pytest.fail(f"queue usage models are missing: {exc}")
    return QueueParameter, QueueUsage, QueueUsageSummary, QueueUsageOutput


def test_queue_usage_models_preserve_parameter_level_hardcoding():
    QueueParameter, QueueUsage, QueueUsageSummary, QueueUsageOutput = _models()

    fixed = QueueParameter(
        name="queue",
        expression='"jobs"',
        value="jobs",
        source_kind="literal",
        hardcoded=True,
    )
    dynamic = QueueParameter(
        name="routing_key",
        expression="settings.ROUTING_KEY",
        value=None,
        source_kind="configuration",
        hardcoded=False,
    )
    usage = QueueUsage(
        category="task_queue",
        framework="celery",
        operation="publish",
        file="tasks.py",
        line=12,
        column=4,
        statement='task.apply_async(queue="jobs")',
        parameters=[fixed, dynamic],
        hardcoding_status="partially_hardcoded",
    )
    summary = QueueUsageSummary(
        total_count=1,
        total_usages=1,
        files_scanned=1,
        scan_duration_ms=1,
        by_category={"task_queue": 1},
        by_framework={"celery": 1},
        hardcoded_parameters=1,
        dynamic_parameters=1,
        unknown_parameters=0,
    )
    output = QueueUsageOutput(summary=summary, results={"task_queue": [usage]})

    assert output.results["task_queue"][0].parameters[0].hardcoded is True
    assert output.results["task_queue"][0].parameters[1].hardcoded is False
    assert output.summary.total_usages == 1
