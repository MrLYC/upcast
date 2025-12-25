"""Tests for base scanner models."""

import json

import pytest
from pydantic import ValidationError

from upcast.models.base import ScannerOutput, ScannerSummary


class TestScannerSummary:
    """Test ScannerSummary base model."""

    def test_valid_summary(self):
        """Test creating a valid summary."""
        summary = ScannerSummary(
            total_count=10,
            files_scanned=5,
            scan_duration_ms=250,
        )
        assert summary.total_count == 10
        assert summary.files_scanned == 5
        assert summary.scan_duration_ms == 250

    def test_summary_without_duration(self):
        """Test creating summary without scan duration."""
        summary = ScannerSummary(
            total_count=10,
            files_scanned=5,
        )
        assert summary.total_count == 10
        assert summary.files_scanned == 5
        assert summary.scan_duration_ms is None

    def test_negative_count_rejected(self):
        """Test that negative counts are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ScannerSummary(
                total_count=-1,
                files_scanned=5,
            )
        errors = exc_info.value.errors()
        assert any("total_count" in str(e) for e in errors)

    def test_negative_files_scanned_rejected(self):
        """Test that negative files_scanned is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ScannerSummary(
                total_count=10,
                files_scanned=-1,
            )
        errors = exc_info.value.errors()
        assert any("files_scanned" in str(e) for e in errors)

    def test_negative_duration_rejected(self):
        """Test that negative scan duration is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ScannerSummary(
                total_count=10,
                files_scanned=5,
                scan_duration_ms=-100,
            )
        errors = exc_info.value.errors()
        assert any("scan_duration_ms" in str(e) for e in errors)

    def test_extra_fields_rejected(self):
        """Test that extra fields are rejected (frozen model)."""
        with pytest.raises(ValidationError):
            ScannerSummary(
                total_count=10,
                files_scanned=5,
                extra_field="not_allowed",  # type: ignore[call-arg]
            )

    def test_summary_is_immutable(self):
        """Test that summary is frozen (immutable)."""
        summary = ScannerSummary(
            total_count=10,
            files_scanned=5,
        )
        with pytest.raises(ValidationError):
            summary.total_count = 999  # type: ignore[misc]


class TestScannerOutput:
    """Test ScannerOutput generic model."""

    def test_valid_output_with_dict_results(self):
        """Test creating output with dict results."""
        summary = ScannerSummary(total_count=2, files_scanned=1)
        output = ScannerOutput[dict[str, str]](
            summary=summary,
            results={"key1": "value1", "key2": "value2"},
        )
        assert output.summary == summary
        assert output.results == {"key1": "value1", "key2": "value2"}
        assert output.metadata == {}

    def test_valid_output_with_list_results(self):
        """Test creating output with list results."""
        summary = ScannerSummary(total_count=3, files_scanned=1)
        output = ScannerOutput[list[str]](
            summary=summary,
            results=["item1", "item2", "item3"],
        )
        assert output.summary == summary
        assert len(output.results) == 3

    def test_output_with_metadata(self):
        """Test creating output with metadata."""
        summary = ScannerSummary(total_count=1, files_scanned=1)
        metadata = {
            "scanner_name": "test-scanner",
            "scanner_version": "1.0.0",
            "scan_timestamp": "2025-12-21T10:00:00Z",
        }
        output = ScannerOutput[dict[str, str]](
            summary=summary,
            results={"key": "value"},
            metadata=metadata,
        )
        assert output.metadata == metadata

    def test_missing_summary_rejected(self):
        """Test that output without summary is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ScannerOutput[dict[str, str]](  # type: ignore[call-arg]
                results={"key": "value"},
            )
        errors = exc_info.value.errors()
        assert any("summary" in str(e) for e in errors)

    def test_missing_results_rejected(self):
        """Test that output without results is rejected."""
        summary = ScannerSummary(total_count=0, files_scanned=0)
        with pytest.raises(ValidationError) as exc_info:
            ScannerOutput[dict[str, str]](  # type: ignore[call-arg]
                summary=summary,
            )
        errors = exc_info.value.errors()
        assert any("results" in str(e) for e in errors)

    def test_to_dict_conversion(self):
        """Test converting output to dictionary."""
        summary = ScannerSummary(total_count=1, files_scanned=1)
        output = ScannerOutput[dict[str, str]](
            summary=summary,
            results={"key": "value"},
            metadata={"scanner": "test"},
        )
        data = output.to_dict()

        assert isinstance(data, dict)
        assert "summary" in data
        assert "results" in data
        assert "metadata" in data
        assert data["summary"]["total_count"] == 1
        assert data["results"]["key"] == "value"

    def test_to_json_conversion(self):
        """Test converting output to JSON."""
        summary = ScannerSummary(total_count=1, files_scanned=1, scan_duration_ms=100)
        output = ScannerOutput[dict[str, str]](
            summary=summary,
            results={"key": "value"},
        )
        json_str = output.to_json()

        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data["summary"]["total_count"] == 1
        assert data["results"]["key"] == "value"

    def test_json_round_trip(self):
        """Test serializing to JSON and deserializing back."""
        summary = ScannerSummary(total_count=5, files_scanned=2)
        original = ScannerOutput[dict[str, int]](
            summary=summary,
            results={"count1": 10, "count2": 20},
            metadata={"version": "1.0"},
        )

        # Serialize to JSON
        json_str = original.to_json()

        # Deserialize back
        restored = ScannerOutput[dict[str, int]].model_validate_json(json_str)

        assert restored.summary.total_count == original.summary.total_count
        assert restored.results == original.results
        assert restored.metadata == original.metadata

    def test_extra_metadata_allowed(self):
        """Test that extra fields in metadata are allowed."""
        summary = ScannerSummary(total_count=1, files_scanned=1)
        # Extra fields at top level should be allowed due to extra="allow"
        output = ScannerOutput[dict[str, str]](
            summary=summary,
            results={"key": "value"},
            metadata={"custom_field": "custom_value", "another": 123},
        )
        assert output.metadata["custom_field"] == "custom_value"
        assert output.metadata["another"] == 123
