"""Tests for common file utilities."""

from pathlib import Path

import pytest

from upcast.common.file_utils import collect_python_files, find_package_root, validate_path


class TestValidatePath:
    """Tests for validate_path function."""

    def test_validates_existing_file(self, tmp_path: Path) -> None:
        """Should validate existing file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("# test")

        result = validate_path(str(test_file))
        assert result == test_file

    def test_validates_existing_directory(self, tmp_path: Path) -> None:
        """Should validate existing directory."""
        result = validate_path(str(tmp_path))
        assert result == tmp_path

    def test_raises_for_nonexistent_path(self) -> None:
        """Should raise FileNotFoundError for nonexistent path."""
        with pytest.raises(FileNotFoundError, match="Path not found"):
            validate_path("/nonexistent/path")


class TestFindPackageRoot:
    """Tests for find_package_root function."""

    def test_finds_package_root(self, tmp_path: Path) -> None:
        """Should find outermost package root."""
        # Create nested package structure
        pkg_root = tmp_path / "mypackage"
        pkg_root.mkdir()
        (pkg_root / "__init__.py").write_text("")

        sub_pkg = pkg_root / "subpackage"
        sub_pkg.mkdir()
        (sub_pkg / "__init__.py").write_text("")

        # Start from subpackage
        result = find_package_root(sub_pkg)
        assert result == pkg_root

    def test_returns_original_without_init(self, tmp_path: Path) -> None:
        """Should return original path if no __init__.py found."""
        result = find_package_root(tmp_path)
        assert result == tmp_path

    def test_handles_file_path(self, tmp_path: Path) -> None:
        """Should handle file path by checking parent."""
        pkg = tmp_path / "pkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")

        test_file = pkg / "module.py"
        test_file.write_text("")

        result = find_package_root(test_file)
        assert result == pkg


class TestCollectPythonFiles:
    """Tests for collect_python_files function."""

    def test_collects_single_file(self, tmp_path: Path) -> None:
        """Should return single file if given file path."""
        test_file = tmp_path / "test.py"
        test_file.write_text("# test")

        result = collect_python_files(test_file)
        assert result == [test_file]

    def test_ignores_non_python_file(self, tmp_path: Path) -> None:
        """Should ignore non-Python files."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        result = collect_python_files(test_file)
        assert result == []

    def test_collects_from_directory(self, tmp_path: Path) -> None:
        """Should recursively collect Python files."""
        (tmp_path / "file1.py").write_text("")
        sub_dir = tmp_path / "subdir"
        sub_dir.mkdir()
        (sub_dir / "file2.py").write_text("")

        result = collect_python_files(tmp_path)
        assert len(result) == 2
        assert all(f.suffix == ".py" for f in result)

    def test_excludes_default_patterns(self, tmp_path: Path) -> None:
        """Should exclude default patterns like __pycache__."""
        (tmp_path / "file.py").write_text("")

        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        (pycache / "cached.py").write_text("")

        result = collect_python_files(tmp_path)
        assert len(result) == 1
        assert result[0].name == "file.py"

    def test_respects_custom_exclude(self, tmp_path: Path) -> None:
        """Should respect custom exclude patterns."""
        (tmp_path / "file1.py").write_text("")
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        (test_dir / "test_file.py").write_text("")

        result = collect_python_files(tmp_path, exclude_patterns=["tests/**"])
        assert len(result) == 1
        assert result[0].name == "file1.py"

    def test_respects_include_patterns(self, tmp_path: Path) -> None:
        """Should only include files matching include patterns."""
        (tmp_path / "model.py").write_text("")
        (tmp_path / "test.py").write_text("")

        result = collect_python_files(tmp_path, include_patterns=["model*.py"])
        assert len(result) == 1
        assert result[0].name == "model.py"

    def test_returns_sorted_list(self, tmp_path: Path) -> None:
        """Should return files in sorted order."""
        (tmp_path / "c.py").write_text("")
        (tmp_path / "a.py").write_text("")
        (tmp_path / "b.py").write_text("")

        result = collect_python_files(tmp_path)
        names = [f.name for f in result]
        assert names == ["a.py", "b.py", "c.py"]
