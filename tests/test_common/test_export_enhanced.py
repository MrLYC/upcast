"""Tests for enhanced export functions."""

import json
from datetime import datetime

import pytest
import yaml

from upcast.common.export import export_scanner_output
from upcast.models.base import ScannerOutput, ScannerSummary


class TestExportScannerOutput:
    """Tests for export_scanner_output function."""

    def test_exports_scanner_output_to_yaml(self, tmp_path):
        """Test exporting ScannerOutput to YAML file."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=5, files_scanned=2),
            results={"items": [{"name": "test1"}, {"name": "test2"}]},
            metadata={},
        )

        output_file = tmp_path / "output.yaml"
        export_scanner_output(output, str(output_file), format="yaml")

        assert output_file.exists()
        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert data["summary"]["total_count"] == 5
        assert data["summary"]["files_scanned"] == 2

    def test_exports_scanner_output_to_json(self, tmp_path):
        """Test exporting ScannerOutput to JSON file."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=3, files_scanned=1),
            results={"items": [{"name": "test1"}]},
            metadata={},
        )

        output_file = tmp_path / "output.json"
        export_scanner_output(output, str(output_file), format="json")

        assert output_file.exists()
        with open(output_file) as f:
            data = json.load(f)

        assert data["summary"]["total_count"] == 3

    def test_exports_dict_to_yaml(self, tmp_path):
        """Test exporting plain dict to YAML file."""
        data = {
            "summary": {"total_count": 2, "files_scanned": 1},
            "results": {"items": [{"name": "test"}]},
        }

        output_file = tmp_path / "output.yaml"
        export_scanner_output(data, str(output_file), format="yaml")

        assert output_file.exists()
        with open(output_file) as f:
            loaded = yaml.safe_load(f)

        assert loaded["summary"]["total_count"] == 2

    def test_injects_scanner_name_metadata(self, tmp_path):
        """Test that scanner name is injected into metadata."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=1, files_scanned=1),
            results={},
            metadata={},
        )

        output_file = tmp_path / "output.yaml"
        export_scanner_output(output, str(output_file), scanner_name="test-scanner", format="yaml")

        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert data["metadata"]["scanner_name"] == "test-scanner"

    def test_injects_scanner_version_metadata(self, tmp_path):
        """Test that scanner version is injected into metadata."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=1, files_scanned=1),
            results={},
            metadata={},
        )

        output_file = tmp_path / "output.yaml"
        export_scanner_output(output, str(output_file), scanner_version="1.0.0", format="yaml")

        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert data["metadata"]["scanner_version"] == "1.0.0"

    def test_injects_timestamp_metadata(self, tmp_path):
        """Test that timestamp is automatically injected."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=1, files_scanned=1),
            results={},
            metadata={},
        )

        output_file = tmp_path / "output.yaml"
        export_scanner_output(output, str(output_file), format="yaml")

        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert "scan_timestamp" in data["metadata"]
        # Verify it's a valid ISO format timestamp
        timestamp = data["metadata"]["scan_timestamp"]
        datetime.fromisoformat(timestamp)  # Should not raise

    def test_skips_metadata_injection_when_disabled(self, tmp_path):
        """Test that metadata injection can be disabled."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=1, files_scanned=1),
            results={},
            metadata={},
        )

        output_file = tmp_path / "output.yaml"
        export_scanner_output(
            output,
            str(output_file),
            scanner_name="test",
            include_metadata=False,
            format="yaml",
        )

        with open(output_file) as f:
            data = yaml.safe_load(f)

        # Metadata should exist but not contain injected fields
        assert "scanner_name" not in data.get("metadata", {})
        assert "scan_timestamp" not in data.get("metadata", {})

    def test_preserves_existing_metadata(self, tmp_path):
        """Test that existing metadata is preserved."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=1, files_scanned=1),
            results={},
            metadata={"custom_field": "custom_value"},
        )

        output_file = tmp_path / "output.yaml"
        export_scanner_output(output, str(output_file), format="yaml")

        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert data["metadata"]["custom_field"] == "custom_value"
        assert "scan_timestamp" in data["metadata"]

    def test_creates_parent_directories(self, tmp_path):
        """Test that parent directories are created if needed."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=1, files_scanned=1),
            results={},
            metadata={},
        )

        output_file = tmp_path / "nested" / "dir" / "output.yaml"
        export_scanner_output(output, str(output_file), format="yaml")

        assert output_file.exists()

    def test_raises_for_invalid_format(self, tmp_path):
        """Test that invalid format raises ValueError."""
        output = ScannerOutput(
            summary=ScannerSummary(total_count=1, files_scanned=1),
            results={},
            metadata={},
        )

        output_file = tmp_path / "output.xml"
        with pytest.raises(ValueError, match="Invalid format"):
            export_scanner_output(output, str(output_file), format="xml")
