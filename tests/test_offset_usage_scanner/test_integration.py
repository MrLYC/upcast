"""Integration tests for static offset usage detection."""

from pathlib import Path

from upcast.scanners.offset_usage import OffsetUsageScanner


FIXTURE = Path(__file__).parent / "fixtures" / "offset_patterns.py"
SETTINGS_FIXTURE = Path(__file__).parent / "fixtures" / "settings.py"


def _findings(output):
    return [finding for findings in output.results.values() for finding in findings]


def test_scanner_detects_queryset_slices_and_parameter_evidence():
    output = OffsetUsageScanner().scan(FIXTURE)

    findings = [finding for finding in _findings(output) if finding.pattern == "queryset_slice"]
    operations = {finding.operation for finding in findings}

    assert operations == {"slice"}
    assert len(findings) == 3

    dynamic = next(finding for finding in findings if finding.offset and finding.offset.expression == "offset")
    assert dynamic.offset.hardcoded is False
    assert dynamic.offset.source_kind == "runtime"
    assert dynamic.limit.expression == "offset + page_size"
    assert dynamic.hardcoding_status == "partially_hardcoded"

    zero = next(finding for finding in findings if finding.offset and finding.offset.expression == "0")
    assert zero.offset.value == 0
    assert zero.offset.hardcoded is True


def test_scanner_detects_django_and_drf_indirect_pagination_but_not_cursor():
    output = OffsetUsageScanner().scan(FIXTURE)
    findings = _findings(output)

    django = [finding for finding in findings if finding.pattern == "django_paginator"]
    page_number = [finding for finding in findings if finding.pattern == "drf_page_number"]
    limit_offset = [finding for finding in findings if finding.pattern == "drf_limit_offset"]

    assert {finding.operation for finding in django} == {"construct", "page"}
    assert len(page_number) == 1
    assert len(limit_offset) == 2
    assert all(finding.hardcoding_status in {"fully_hardcoded", "partially_hardcoded", "unknown"} for finding in django)
    assert not any(finding.pattern == "drf_cursor" for finding in findings)


def test_scanner_detects_static_and_dynamic_raw_sql_offset():
    output = OffsetUsageScanner().scan(FIXTURE)
    findings = [finding for finding in _findings(output) if finding.pattern == "raw_sql"]

    assert len(findings) == 3
    assert {finding.operation for finding in findings} == {"raw", "raw_sql", "execute"}
    assert any(finding.offset and finding.offset.hardcoded is True for finding in findings)
    assert any(finding.offset and finding.offset.hardcoded is False for finding in findings)


def test_scanner_summary_is_grouped_and_ordinary_slices_are_ignored():
    output = OffsetUsageScanner().scan(FIXTURE)

    assert output.summary.total_count == len(_findings(output))
    assert output.summary.by_pattern["queryset_slice"] == 3
    assert output.summary.by_framework["django"] >= 2
    assert output.summary.direct_offset_count >= 3
    assert output.summary.indirect_pagination_count >= 3
    assert all(finding.file == "offset_patterns.py" for finding in _findings(output))


def test_scanner_detects_default_drf_pagination_settings():
    output = OffsetUsageScanner().scan(SETTINGS_FIXTURE)

    findings = [finding for finding in _findings(output) if finding.pattern == "drf_page_number"]

    assert len(findings) == 1
    assert findings[0].operation == "configure"
    assert findings[0].page_size is not None
    assert findings[0].page_size.value == 100
    assert findings[0].page_size.hardcoded is True
