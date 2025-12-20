"""Tests for AST utilities."""

from pathlib import Path
from textwrap import dedent

from astroid import MANAGER, nodes

from upcast.django_model_scanner.ast_utils import (
    infer_literal_value,
    is_django_field,
    is_django_model,
    safe_as_string,
)


class TestIsDjangoModel:
    """Test is_django_model function."""

    def test_direct_model_inheritance(self, tmp_path: Path) -> None:
        """Test detecting direct Model inheritance."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class TestModel(models.Model):
                    pass
                """
            )
        )

        module = MANAGER.ast_from_file(str(models_file), modname="models")

        for node in module.nodes_of_class(nodes.ClassDef):
            if node.name == "TestModel":
                assert is_django_model(node) is True

    def test_non_model_class(self, tmp_path: Path) -> None:
        """Test non-model class is not detected."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                class RegularClass:
                    pass
                """
            )
        )

        module = MANAGER.ast_from_file(str(models_file), modname="models")

        for node in module.nodes_of_class(nodes.ClassDef):
            if node.name == "RegularClass":
                assert is_django_model(node) is False


class TestIsDjangoField:
    """Test is_django_field function."""

    def test_detect_char_field(self, tmp_path: Path) -> None:
        """Test detecting CharField."""
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

        for class_node in module.nodes_of_class(nodes.ClassDef):
            if class_node.name == "TestModel":
                for node in class_node.body:
                    if isinstance(node, nodes.Assign):
                        assert is_django_field(node) is True


class TestInferLiteralValue:
    """Test infer_literal_value function."""

    def test_infer_int(self, tmp_path: Path) -> None:
        """Test inferring integer value."""
        test_file = tmp_path / "test.py"
        test_file.write_text("value = 42")

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.body:
            if isinstance(node, nodes.Assign):
                result = infer_literal_value(node.value)
                assert result == 42

    def test_infer_string(self, tmp_path: Path) -> None:
        """Test inferring string value."""
        test_file = tmp_path / "test.py"
        test_file.write_text('value = "hello"')

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.body:
            if isinstance(node, nodes.Assign):
                result = infer_literal_value(node.value)
                assert result == "hello"

    def test_infer_bool(self, tmp_path: Path) -> None:
        """Test inferring boolean value."""
        test_file = tmp_path / "test.py"
        test_file.write_text("value = True")

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.body:
            if isinstance(node, nodes.Assign):
                result = infer_literal_value(node.value)
                assert result is True


class TestSafeAsString:
    """Test safe_as_string function."""

    def test_safe_as_string_simple(self, tmp_path: Path) -> None:
        """Test converting simple node to string."""
        test_file = tmp_path / "test.py"
        test_file.write_text("value = 123")

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.body:
            if isinstance(node, nodes.Assign):
                result = safe_as_string(node.value)
                assert isinstance(result, str)
                assert "123" in result

    def test_safe_as_string_handles_errors(self, tmp_path: Path) -> None:
        """Test safe_as_string handles errors gracefully."""
        test_file = tmp_path / "test.py"
        test_file.write_text("value = complex_function()")

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.body:
            if isinstance(node, nodes.Assign):
                # Should not raise exception
                result = safe_as_string(node.value)
                assert isinstance(result, str)
