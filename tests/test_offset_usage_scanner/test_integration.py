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


def test_scanner_does_not_treat_list_named_qs_as_a_queryset(tmp_path: Path):
    source = tmp_path / "ordinary.py"
    source.write_text(
        """
from app.models import User

qs = [1, 2, 3, 4]
queryset = (1, 2, 3, 4)
list_window = qs[1:3]
tuple_window = queryset[1:3]
orm_qs = User.objects.order_by("id")
orm_window = orm_qs[1:3]
""",
        encoding="utf-8",
    )

    output = OffsetUsageScanner().scan(tmp_path)

    findings = _findings(output)

    assert len(findings) == 1
    assert findings[0].pattern == "queryset_slice"
    assert findings[0].offset is not None
    assert findings[0].offset.expression == "1"


def test_scanner_tracks_queryset_attributes_and_filter_queryset_results(tmp_path: Path):
    source = tmp_path / "views.py"
    source.write_text(
        """
from app.models import User

class UserView:
    def get(self):
        queryset = self.queryset
        from_attribute = queryset[1:3]
        filtered = self.filter_queryset(User.objects.all())
        from_filter = filtered[2:4]
""",
        encoding="utf-8",
    )

    output = OffsetUsageScanner().scan(tmp_path)

    findings = _findings(output)

    assert len(findings) == 2
    assert [finding.offset.value for finding in findings if finding.offset is not None] == [1, 2]


def test_scanner_detects_default_drf_pagination_settings():
    output = OffsetUsageScanner().scan(SETTINGS_FIXTURE)

    findings = [finding for finding in _findings(output) if finding.pattern == "drf_page_number"]

    assert len(findings) == 1
    assert findings[0].operation == "configure"
    assert findings[0].page_size is not None
    assert findings[0].page_size.value == 100
    assert findings[0].page_size.hardcoded is True
