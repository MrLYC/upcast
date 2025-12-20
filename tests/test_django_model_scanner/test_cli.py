"""Tests for CLI functionality."""

from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from upcast.django_model_scanner.checker import DjangoModelChecker
from upcast.django_model_scanner.cli import (
    _find_project_root,
    _scan_file,
    scan_django_models,
)


class TestFindProjectRoot:
    """Test _find_project_root function."""

    def test_find_src_directory(self, tmp_path: Path) -> None:
        """Test finding src/ directory with Python packages."""
        # Create src/ directory with __init__.py
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        package_dir = src_dir / "myapp"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("")

        result = _find_project_root(tmp_path, verbose=False)
        assert result == str(src_dir)

    def test_no_src_directory(self, tmp_path: Path) -> None:
        """Test when no src/ directory exists."""
        result = _find_project_root(tmp_path, verbose=False)
        assert result == str(tmp_path)

    def test_src_without_packages(self, tmp_path: Path) -> None:
        """Test src/ directory without Python packages."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        # No __init__.py files

        result = _find_project_root(tmp_path, verbose=False)
        assert result == str(tmp_path)

    def test_from_file_path(self, tmp_path: Path) -> None:
        """Test finding root from file path."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        package_dir = src_dir / "myapp"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("")

        # Create a test file
        test_file = package_dir / "models.py"
        test_file.write_text("# test")

        # _find_project_root starts from the directory containing the file
        result = _find_project_root(test_file, verbose=False)
        # It should find src/ by going up from package_dir
        assert result == str(src_dir)


# Removed _collect_python_files test - now using common.file_utils.collect_python_files
# which is tested in tests/test_common/test_file_utils.py


class TestScanFile:
    """Test _scan_file function."""

    def test_scan_simple_model(self, tmp_path: Path) -> None:
        """Test scanning a file with a simple model."""
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

        checker = DjangoModelChecker(root_path=str(tmp_path))
        _scan_file(models_file, checker, verbose=False)

        models = checker.get_models()
        assert len(models) > 0

    def test_scan_file_with_syntax_error(self, tmp_path: Path) -> None:
        """Test scanning file with syntax error raises exception."""
        from astroid import AstroidSyntaxError

        bad_file = tmp_path / "bad.py"
        bad_file.write_text("this is not valid python {{{")

        checker = DjangoModelChecker(root_path=str(tmp_path))

        with pytest.raises(AstroidSyntaxError):
            _scan_file(bad_file, checker, verbose=False)


class TestScanDjangoModels:
    """Test scan_django_models function."""

    def test_scan_directory(self, tmp_path: Path) -> None:
        """Test scanning a directory."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class Author(models.Model):
                    name = models.CharField(max_length=100)
                """
            )
        )

        result = scan_django_models(str(tmp_path))
        assert result
        models = yaml.safe_load(result)
        assert len(models) > 0

    def test_scan_single_file(self, tmp_path: Path) -> None:
        """Test scanning a single file."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class Book(models.Model):
                    title = models.CharField(max_length=200)
                """
            )
        )

        result = scan_django_models(str(models_file))
        assert result
        models = yaml.safe_load(result)
        assert len(models) > 0

    def test_scan_with_output_file(self, tmp_path: Path) -> None:
        """Test scanning with output file."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class Product(models.Model):
                    name = models.CharField(max_length=100)
                """
            )
        )

        output_file = tmp_path / "output.yaml"
        result = scan_django_models(str(tmp_path), output=str(output_file))

        # Should return empty string when writing to file
        assert result == ""

        # File should exist with valid YAML
        assert output_file.exists()
        with open(output_file) as f:
            models = yaml.safe_load(f)
        assert len(models) > 0

    def test_scan_nonexistent_path(self) -> None:
        """Test scanning nonexistent path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            scan_django_models("/nonexistent/path")

    def test_scan_empty_directory(self, tmp_path: Path) -> None:
        """Test scanning empty directory returns empty result."""
        result = scan_django_models(str(tmp_path))
        assert result == ""

    def test_verbose_output(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test verbose output is printed to stderr."""
        models_file = tmp_path / "models.py"
        models_file.write_text(
            dedent(
                """
                from django.db import models

                class TestModel(models.Model):
                    field = models.CharField(max_length=50)
                """
            )
        )

        scan_django_models(str(tmp_path), verbose=True)

        captured = capsys.readouterr()
        assert "Scanning" in captured.err
        assert "Found" in captured.err
