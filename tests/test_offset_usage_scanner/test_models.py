"""Contract tests for offset usage output models."""

import pytest


def _models():
    try:
        from upcast.models.offset_usage import (
            OffsetParameter,
            OffsetUsage,
            OffsetUsageOutput,
            OffsetUsageSummary,
        )
    except ModuleNotFoundError as exc:
        pytest.fail(f"offset usage models are missing: {exc}")
    return OffsetParameter, OffsetUsage, OffsetUsageSummary, OffsetUsageOutput


def test_offset_usage_models_preserve_parameter_evidence_and_output_shape():
    OffsetParameter, OffsetUsage, OffsetUsageSummary, OffsetUsageOutput = _models()

    offset = OffsetParameter(
        name="offset",
        expression="(page - 1) * page_size",
        value=None,
        source_kind="expression",
        hardcoded=None,
    )
    page_size = OffsetParameter(
        name="page_size",
        expression="settings.PAGE_SIZE",
        value=None,
        source_kind="configuration",
        hardcoded=False,
    )
    usage = OffsetUsage(
        pattern="queryset_slice",
        framework="django",
        operation="slice",
        file="views.py",
        line=18,
        column=11,
        statement="queryset[(page - 1) * page_size : page * page_size]",
        function="list_users",
        parameters=[offset, page_size],
        offset=offset,
        page_size=page_size,
        hardcoding_status="dynamic",
    )
    summary = OffsetUsageSummary(
        total_count=1,
        files_scanned=1,
        scan_duration_ms=1,
        by_pattern={"queryset_slice": 1},
        by_framework={"django": 1},
        direct_offset_count=1,
        indirect_pagination_count=0,
        dynamic_count=1,
    )
    output = OffsetUsageOutput(summary=summary, results={"queryset_slice": [usage]})

    assert output.results["queryset_slice"][0].offset is offset
    assert output.results["queryset_slice"][0].page_size is page_size
    assert output.results["queryset_slice"][0].parameters[0].hardcoded is None
    assert output.summary.total_count == 1


def test_offset_usage_models_allow_static_and_unknown_parameter_values():
    OffsetParameter, OffsetUsage, OffsetUsageSummary, OffsetUsageOutput = _models()

    fixed = OffsetParameter(
        name="limit",
        expression="50",
        value=50,
        source_kind="literal",
        hardcoded=True,
    )
    unknown = OffsetParameter(
        name="page",
        expression="request.GET.get('page')",
        value=None,
        source_kind="runtime",
        hardcoded=False,
    )

    assert fixed.value == 50
    assert fixed.hardcoded is True
    assert unknown.value is None
    assert unknown.hardcoded is False
