"""Tests for export functionality."""

from pathlib import Path

import yaml

from upcast.django_model_scanner.export import (
    export_to_yaml,
    export_to_yaml_string,
    format_model_output,
)


class TestFormatModelOutput:
    """Test format_model_output function."""

    def test_format_simple_model(self) -> None:
        """Test formatting a simple model."""
        model_data = {
            "name": "TestModel",
            "module": "myapp.models",
            "abstract": False,
            "bases": ["django.db.models.base.Model"],
            "fields": {
                "name": {
                    "type": "CharField",
                    "max_length": 100,
                }
            },
            "relationships": {},
            "meta": {"db_table": "test_model"},
        }

        result = format_model_output({"myapp.models.TestModel": model_data})

        # Should be a dict
        assert isinstance(result, dict)
        assert "myapp.models.TestModel" in result

    def test_format_includes_bases(self) -> None:
        """Test that formatted output includes bases field."""
        model_data = {
            "name": "TestModel",
            "module": "myapp.models",
            "abstract": False,
            "bases": ["django.db.models.base.Model"],
            "fields": {},
            "relationships": {},
            "meta": {},
        }

        result = format_model_output({"myapp.models.TestModel": model_data})

        assert "bases" in result["myapp.models.TestModel"]

    def test_format_includes_description(self) -> None:
        """Test that formatted output includes description field from docstring."""
        model_data = {
            "name": "TestModel",
            "module": "myapp.models",
            "description": "This is a test model for user data.",
            "abstract": False,
            "bases": ["django.db.models.base.Model"],
            "fields": {},
            "relationships": {},
            "meta": {},
        }

        result = format_model_output({"myapp.models.TestModel": model_data})

        assert "description" in result["myapp.models.TestModel"]
        assert result["myapp.models.TestModel"]["description"] == "This is a test model for user data."

    def test_format_without_description(self) -> None:
        """Test that models without docstring don't have description field."""
        model_data = {
            "name": "TestModel",
            "module": "myapp.models",
            "abstract": False,
            "bases": ["django.db.models.base.Model"],
            "fields": {},
            "relationships": {},
            "meta": {},
        }

        result = format_model_output({"myapp.models.TestModel": model_data})

        # Description should not be in output if not present in model_data
        assert "description" not in result["myapp.models.TestModel"]


class TestExportToYamlString:
    """Test export_to_yaml_string function."""

    def test_export_to_yaml_string(self) -> None:
        """Test exporting to YAML string."""
        models = {
            "myapp.models.TestModel": {
                "name": "TestModel",
                "module": "myapp.models",
                "abstract": False,
                "bases": [],
                "fields": {"name": {"type": "CharField", "max_length": 100}},
                "relationships": {},
                "meta": {},
            }
        }

        result = export_to_yaml_string(models)

        assert isinstance(result, str)
        assert len(result) > 0

        # Should be valid YAML
        parsed = yaml.safe_load(result)
        assert "myapp.models.TestModel" in parsed


class TestExportToYaml:
    """Test export_to_yaml function."""

    def test_export_to_file(self, tmp_path: Path) -> None:
        """Test exporting to YAML file."""
        models = {
            "myapp.models.TestModel": {
                "name": "TestModel",
                "module": "myapp.models",
                "abstract": False,
                "bases": [],
                "fields": {"name": {"type": "CharField", "max_length": 100}},
                "relationships": {},
                "meta": {},
            }
        }

        output_file = tmp_path / "output.yaml"
        export_to_yaml(models, str(output_file))

        # File should exist
        assert output_file.exists()

        # Should contain valid YAML
        with open(output_file) as f:
            parsed = yaml.safe_load(f)
        assert "myapp.models.TestModel" in parsed

    def test_export_creates_directories(self, tmp_path: Path) -> None:
        """Test that export creates parent directories."""
        output_file = tmp_path / "subdir" / "output.yaml"
        models = {
            "myapp.models.TestModel": {
                "name": "TestModel",
                "module": "myapp.models",
                "abstract": False,
                "bases": [],
                "fields": {},
                "relationships": {},
                "meta": {},
            }
        }

        export_to_yaml(models, str(output_file))

        assert output_file.exists()
