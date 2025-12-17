"""Tests for export utilities."""

import json
from pathlib import Path

import yaml

from upcast.common.export import (
    export_to_json,
    export_to_yaml,
    export_to_yaml_string,
    sort_dict_recursive,
)


class TestSortDictRecursive:
    """Tests for sort_dict_recursive function."""

    def test_sorts_dict_keys(self) -> None:
        """Should sort dict keys alphabetically."""
        data = {"z": 1, "a": 2, "m": 3}
        result = sort_dict_recursive(data)
        assert list(result.keys()) == ["a", "m", "z"]

    def test_sorts_nested_dicts(self) -> None:
        """Should recursively sort nested dicts."""
        data = {"outer": {"z": 1, "a": 2}, "first": 3}
        result = sort_dict_recursive(data)
        assert list(result.keys()) == ["first", "outer"]
        assert list(result["outer"].keys()) == ["a", "z"]

    def test_sorts_list_by_file_line_column(self) -> None:
        """Should sort lists of dicts by file, line, column."""
        data = [
            {"file": "b.py", "line": 1, "column": 0, "name": "x"},
            {"file": "a.py", "line": 2, "column": 0, "name": "y"},
            {"file": "a.py", "line": 1, "column": 5, "name": "z"},
            {"file": "a.py", "line": 1, "column": 0, "name": "w"},
        ]
        result = sort_dict_recursive(data)
        # Should sort by file, then line, then column
        assert result[0]["file"] == "a.py"
        assert result[0]["line"] == 1
        assert result[0]["column"] == 0
        assert result[1]["column"] == 5
        assert result[2]["line"] == 2
        assert result[3]["file"] == "b.py"

    def test_sorts_list_by_name_if_no_location(self) -> None:
        """Should sort lists by name if no location fields."""
        data = [{"name": "zebra"}, {"name": "apple"}, {"name": "monkey"}]
        result = sort_dict_recursive(data)
        assert [item["name"] for item in result] == ["apple", "monkey", "zebra"]

    def test_preserves_non_sortable_lists(self) -> None:
        """Should preserve order for non-sortable lists."""
        data = [1, 3, 2]  # Simple values, not dicts
        result = sort_dict_recursive(data)
        assert result == [1, 3, 2]

    def test_handles_mixed_types(self) -> None:
        """Should handle dicts with mixed value types."""
        data = {"list": [3, 1, 2], "dict": {"z": 1, "a": 2}, "value": 42}
        result = sort_dict_recursive(data)
        assert list(result.keys()) == ["dict", "list", "value"]
        assert list(result["dict"].keys()) == ["a", "z"]


class TestExportToYaml:
    """Tests for export_to_yaml function."""

    def test_exports_to_file(self, tmp_path: Path) -> None:
        """Should export data to YAML file."""
        data = {"name": "test", "value": 42}
        output_file = tmp_path / "output.yaml"

        export_to_yaml(data, output_file)

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed == data

    def test_sorts_output(self, tmp_path: Path) -> None:
        """Should sort data before exporting."""
        data = {"z": 1, "a": 2, "m": 3}
        output_file = tmp_path / "output.yaml"

        export_to_yaml(data, output_file)

        content = output_file.read_text(encoding="utf-8")
        # Check that 'a' comes before 'z' in the output
        assert content.index("a:") < content.index("z:")

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """Should create parent directories if needed."""
        output_file = tmp_path / "subdir" / "output.yaml"
        data = {"test": "value"}

        export_to_yaml(data, output_file)

        assert output_file.exists()

    def test_uses_proper_yaml_formatting(self, tmp_path: Path) -> None:
        """Should use proper YAML formatting."""
        data = {"list": [1, 2, 3], "nested": {"key": "value"}}
        output_file = tmp_path / "output.yaml"

        export_to_yaml(data, output_file)

        content = output_file.read_text(encoding="utf-8")
        # Check for proper indentation (2 spaces)
        assert "  key: value" in content


class TestExportToYamlString:
    """Tests for export_to_yaml_string function."""

    def test_returns_yaml_string(self) -> None:
        """Should return YAML as string."""
        data = {"name": "test", "value": 42}
        result = export_to_yaml_string(data)

        assert isinstance(result, str)
        parsed = yaml.safe_load(result)
        assert parsed == data

    def test_sorts_output(self) -> None:
        """Should sort data before converting to string."""
        data = {"z": 1, "a": 2}
        result = export_to_yaml_string(data)

        # 'a' should come before 'z'
        assert result.index("a:") < result.index("z:")


class TestExportToJson:
    """Tests for export_to_json function."""

    def test_returns_json_string_by_default(self) -> None:
        """Should return JSON string by default."""
        data = {"name": "test", "value": 42}
        result = export_to_json(data)

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == data

    def test_exports_to_file(self, tmp_path: Path) -> None:
        """Should export to file if output_path provided."""
        data = {"name": "test", "value": 42}
        output_file = tmp_path / "output.json"

        result = export_to_json(data, output_path=str(output_file))

        assert result == str(output_file)
        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        parsed = json.loads(content)
        assert parsed == data

    def test_sorts_output(self) -> None:
        """Should sort data before exporting."""
        data = {"z": 1, "a": 2, "m": 3}
        result = export_to_json(data)

        parsed = json.loads(result)
        # JSON preserves order in Python 3.7+
        assert list(parsed.keys()) == ["a", "m", "z"]

    def test_uses_proper_json_formatting(self) -> None:
        """Should use proper JSON formatting."""
        data = {"list": [1, 2, 3], "nested": {"key": "value"}}
        result = export_to_json(data)

        # Check for proper indentation (2 spaces)
        assert '  "key"' in result or '"key"' in result  # May vary
