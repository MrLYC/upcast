"""Tests for model parser functionality."""

from pathlib import Path
from textwrap import dedent

import pytest
from astroid import MANAGER

from upcast.django_model_scanner.model_parser import (
    _extract_field_type,
    _is_relationship_field,
    merge_abstract_fields,
    parse_meta_class,
    parse_model,
)


@pytest.fixture
def simple_model_module(tmp_path: Path):
    """Create a simple Django model module."""
    models_file = tmp_path / "models.py"
    models_file.write_text(
        dedent(
            """
            from django.db import models

            class TestModel(models.Model):
                name = models.CharField(max_length=100)
                age = models.IntegerField(default=0)

                class Meta:
                    db_table = "test_models"
            """
        )
    )
    module = MANAGER.ast_from_file(str(models_file), modname="models")
    return module


class TestParseModel:
    """Test parse_model function."""

    def test_parse_basic_model(self, simple_model_module) -> None:
        """Test parsing a basic model."""
        from astroid import nodes

        # Find the TestModel class
        for node in simple_model_module.nodes_of_class(nodes.ClassDef):
            if node.name == "TestModel":
                result = parse_model(node)

                assert result is not None
                assert result["name"] == "TestModel"
                assert "module" in result
                assert "fields" in result
                assert "name" in result["fields"]
                assert "age" in result["fields"]
                break

    def test_parse_model_with_meta(self, simple_model_module) -> None:
        """Test parsing model Meta options."""
        from astroid import nodes

        for node in simple_model_module.nodes_of_class(nodes.ClassDef):
            if node.name == "TestModel":
                result = parse_model(node)

                assert result is not None
                assert "meta" in result
                assert result["meta"]["db_table"] == "test_models"
                break


class TestExtractFieldType:
    """Test _extract_field_type function."""

    def test_extract_char_field(self, tmp_path: Path) -> None:
        """Test extracting CharField type."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class TestModel(models.Model):
                    name = models.CharField(max_length=100)
                """
            )
        )
        module = MANAGER.ast_from_file(str(models_file), modname="models")

        from astroid import nodes

        for class_node in module.nodes_of_class(nodes.ClassDef):
            if class_node.name == "TestModel":
                for node in class_node.body:
                    if isinstance(node, nodes.Assign) and isinstance(node.value, nodes.Call):
                        field_type = _extract_field_type(node.value)
                        assert field_type is not None
                        assert field_type == "CharField"
                        break


class TestIsRelationshipField:
    """Test _is_relationship_field function."""

    def test_foreign_key_is_relationship(self) -> None:
        """Test ForeignKey is detected as relationship field."""
        assert _is_relationship_field("django.db.models.fields.related.ForeignKey") is True
        assert _is_relationship_field("ForeignKey") is True

    def test_one_to_one_is_relationship(self) -> None:
        """Test OneToOneField is detected as relationship field."""
        assert _is_relationship_field("OneToOneField") is True

    def test_many_to_many_is_relationship(self) -> None:
        """Test ManyToManyField is detected as relationship field."""
        assert _is_relationship_field("ManyToManyField") is True

    def test_char_field_not_relationship(self) -> None:
        """Test CharField is not detected as relationship field."""
        assert _is_relationship_field("CharField") is False
        assert _is_relationship_field("IntegerField") is False


class TestMergeAbstractFields:
    """Test merge_abstract_fields function."""

    def test_merge_single_abstract_parent(self, tmp_path: Path) -> None:
        """Test merging fields from single abstract parent."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class AbstractModel(models.Model):
                    created_at = models.DateTimeField(auto_now_add=True)

                    class Meta:
                        abstract = True

                class ConcreteModel(AbstractModel):
                    name = models.CharField(max_length=100)
                """
            )
        )
        module = MANAGER.ast_from_file(str(models_file), modname="models")

        from astroid import nodes

        models_dict = {}
        for class_node in module.nodes_of_class(nodes.ClassDef):
            if class_node.name in ["AbstractModel", "ConcreteModel"]:
                result = parse_model(class_node)
                if result:
                    models_dict[class_node.qname()] = result

        # Merge abstract fields
        for _qname, model in models_dict.items():
            if not model.get("abstract", False):
                merge_abstract_fields(model, models_dict)

        # Check that ConcreteModel has both fields
        concrete = next(m for m in models_dict.values() if m["name"] == "ConcreteModel")
        assert "name" in concrete["fields"]
        assert "created_at" in concrete["fields"]


class TestParseMetaClass:
    """Test parse_meta_class function."""

    def test_parse_db_table(self, tmp_path: Path) -> None:
        """Test parsing db_table from Meta."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class TestModel(models.Model):
                    class Meta:
                        db_table = "custom_table"
                """
            )
        )
        module = MANAGER.ast_from_file(str(models_file), modname="models")

        from astroid import nodes

        for class_node in module.nodes_of_class(nodes.ClassDef):
            if class_node.name == "TestModel":
                meta_options = parse_meta_class(class_node)
                assert "db_table" in meta_options
                assert meta_options["db_table"] == "custom_table"
                break

    def test_parse_ordering(self, tmp_path: Path) -> None:
        """Test parsing ordering from Meta."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class TestModel(models.Model):
                    class Meta:
                        ordering = ["-created_at", "name"]
                """
            )
        )
        module = MANAGER.ast_from_file(str(models_file), modname="models")

        from astroid import nodes

        for class_node in module.nodes_of_class(nodes.ClassDef):
            if class_node.name == "TestModel":
                meta_options = parse_meta_class(class_node)
                assert "ordering" in meta_options
                assert isinstance(meta_options["ordering"], list)
                break
