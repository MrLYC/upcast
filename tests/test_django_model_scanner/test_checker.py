"""Tests for checker functionality."""

from pathlib import Path
from textwrap import dedent

from astroid import MANAGER

from upcast.django_model_scanner.checker import DjangoModelChecker


class TestDjangoModelChecker:
    """Test DjangoModelChecker class."""

    def test_visit_classdef(self, tmp_path: Path) -> None:
        """Test visiting Django model class."""
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
        checker = DjangoModelChecker(root_path=str(tmp_path))

        from astroid import nodes

        for node in module.nodes_of_class(nodes.ClassDef):
            checker.visit_classdef(node)

        models = checker.get_models()
        assert len(models) > 0

    def test_close_merges_abstract_fields(self, tmp_path: Path) -> None:
        """Test that close() merges abstract fields."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class BaseModel(models.Model):
                    created_at = models.DateTimeField(auto_now_add=True)

                    class Meta:
                        abstract = True

                class ConcreteModel(BaseModel):
                    name = models.CharField(max_length=100)
                """
            )
        )

        module = MANAGER.ast_from_file(str(models_file), modname="models")
        checker = DjangoModelChecker(root_path=str(tmp_path))

        from astroid import nodes

        for node in module.nodes_of_class(nodes.ClassDef):
            checker.visit_classdef(node)

        # Before close, ConcreteModel might not have inherited fields
        # After close, it should have them
        checker.close()

        models = checker.get_models()
        concrete = next((m for m in models.values() if m["name"] == "ConcreteModel"), None)

        assert concrete is not None
        assert "name" in concrete["fields"]
        assert "created_at" in concrete["fields"]

    def test_get_models(self, tmp_path: Path) -> None:
        """Test get_models returns collected models."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class Model1(models.Model):
                    field1 = models.CharField(max_length=100)

                class Model2(models.Model):
                    field2 = models.IntegerField()
                """
            )
        )

        module = MANAGER.ast_from_file(str(models_file), modname="models")
        checker = DjangoModelChecker(root_path=str(tmp_path))

        from astroid import nodes

        for node in module.nodes_of_class(nodes.ClassDef):
            checker.visit_classdef(node)

        models = checker.get_models()
        assert len(models) >= 2
