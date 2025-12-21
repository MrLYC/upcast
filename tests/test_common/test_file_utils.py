"""Tests for common file utilities."""

from pathlib import Path

import pytest

from upcast.common.file_utils import (
    collect_python_files,
    find_package_root,
    get_relative_path_str,
    is_test_file,
    validate_path,
)


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


class TestGetRelativePathStr:
    """Tests for get_relative_path_str function."""

    def test_returns_relative_path_when_under_base(self, tmp_path: Path) -> None:
        """Should return relative path when file is under base_path."""
        file_path = tmp_path / "src" / "app.py"
        relative = get_relative_path_str(file_path, tmp_path)
        assert relative == "src/app.py"

    def test_returns_absolute_path_when_not_relative(self, tmp_path: Path) -> None:
        """Should return absolute path when file is not under base_path."""
        other_path = Path("/other/location/file.py")
        result = get_relative_path_str(other_path, tmp_path)
        assert result == str(other_path)

    def test_handles_same_path(self, tmp_path: Path) -> None:
        """Should handle when file_path equals base_path."""
        result = get_relative_path_str(tmp_path, tmp_path)
        assert result == "."


class TestIsTestFile:
    """Tests for is_test_file function."""

    def test_identifies_test_prefix(self) -> None:
        """Should identify files with test_ prefix."""
        assert is_test_file(Path("test_app.py"))
        assert is_test_file(Path("src/test_utils.py"))

    def test_identifies_test_suffix(self) -> None:
        """Should identify files with _test suffix."""
        assert is_test_file(Path("app_test.py"))
        assert is_test_file(Path("src/utils_test.py"))

    def test_identifies_tests_directory(self) -> None:
        """Should identify files in tests/ directory."""
        assert is_test_file(Path("tests/test_app.py"))
        assert is_test_file(Path("tests/app.py"))
        assert is_test_file(Path("src/tests/utils.py"))

    def test_does_not_identify_regular_files(self) -> None:
        """Should not identify regular files as test files."""
        assert not is_test_file(Path("app.py"))
        assert not is_test_file(Path("src/utils.py"))
        assert not is_test_file(Path("models.py"))

    def test_does_not_match_partial_names(self) -> None:
        """Should not match files with 'test' in the middle."""
        assert not is_test_file(Path("attest.py"))
        assert not is_test_file(Path("contest.py"))
