"""Tests for BaseScanner abstract class."""

import tempfile
from pathlib import Path

import pytest

from upcast.common.scanner_base import BaseScanner
from upcast.models.base import ScannerOutput, ScannerSummary


class ConcreteTestScanner(BaseScanner[ScannerOutput[list[str]]]):
    """Concrete implementation of BaseScanner for testing."""

    def scan(self, path: Path) -> ScannerOutput[list[str]]:
        """Scan implementation that returns file paths."""
        files = self.get_files_to_scan(path)
        results = [str(f) for f in files]

        summary = ScannerSummary(
            total_count=len(results),
            files_scanned=len(files),
        )

        return ScannerOutput[list[str]](
            summary=summary,
            results=results,
        )

    def scan_file(self, file_path: Path) -> str:
        """Return file path as string."""
        return str(file_path)


class TestBaseScanner:
    """Test BaseScanner functionality."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that BaseScanner cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseScanner()  # type: ignore[abstract]

    def test_default_include_patterns(self):
        """Test default include patterns."""
        scanner = ConcreteTestScanner()
        assert scanner.include_patterns == ["**/*.py"]
        assert scanner.exclude_patterns == []
        assert scanner.verbose is False

    def test_custom_patterns(self):
        """Test custom include/exclude patterns."""
        scanner = ConcreteTestScanner(
            include_patterns=["**/*.py", "**/*.pyi"],
            exclude_patterns=["**/test_*.py", "**/conftest.py"],
            verbose=True,
        )
        assert scanner.include_patterns == ["**/*.py", "**/*.pyi"]
        assert scanner.exclude_patterns == ["**/test_*.py", "**/conftest.py"]
        assert scanner.verbose is True

    def test_should_scan_file_with_include_pattern(self):
        """Test file filtering with include pattern."""
        scanner = ConcreteTestScanner(include_patterns=["**/*.py"])

        assert scanner.should_scan_file(Path("test.py"))
        assert scanner.should_scan_file(Path("dir/test.py"))
        assert not scanner.should_scan_file(Path("test.txt"))
        assert not scanner.should_scan_file(Path("test.md"))

    def test_should_scan_file_with_exclude_pattern(self):
        """Test file filtering with exclude pattern."""
        scanner = ConcreteTestScanner(
            include_patterns=["**/*.py"],
            exclude_patterns=["**/test_*.py"],
        )

        assert scanner.should_scan_file(Path("main.py"))
        assert scanner.should_scan_file(Path("dir/utils.py"))
        assert not scanner.should_scan_file(Path("test_main.py"))
        assert not scanner.should_scan_file(Path("dir/test_utils.py"))

    def test_should_scan_file_multiple_excludes(self):
        """Test file filtering with multiple exclude patterns."""
        scanner = ConcreteTestScanner(
            include_patterns=["**/*.py"],
            exclude_patterns=["**/test_*.py", "**/conftest.py", "**/__pycache__/**"],
        )

        assert scanner.should_scan_file(Path("main.py"))
        assert not scanner.should_scan_file(Path("test_main.py"))
        assert not scanner.should_scan_file(Path("conftest.py"))
        assert not scanner.should_scan_file(Path("__pycache__/module.py"))

    def test_get_files_to_scan_with_single_file(self):
        """Test get_files_to_scan with a single file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("# test")

            scanner = ConcreteTestScanner()
            files = scanner.get_files_to_scan(test_file)

            assert len(files) == 1
            assert files[0] == test_file

    def test_get_files_to_scan_excludes_single_file(self):
        """Test that single file can be excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_main.py"
            test_file.write_text("# test")

            scanner = ConcreteTestScanner(exclude_patterns=["**/test_*.py"])
            files = scanner.get_files_to_scan(test_file)

            assert len(files) == 0

    def test_get_files_to_scan_with_directory(self):
        """Test get_files_to_scan with a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "main.py").write_text("# main")
            (tmppath / "utils.py").write_text("# utils")
            (tmppath / "readme.md").write_text("# readme")

            subdir = tmppath / "subdir"
            subdir.mkdir()
            (subdir / "module.py").write_text("# module")

            scanner = ConcreteTestScanner(include_patterns=["**/*.py"])
            files = scanner.get_files_to_scan(tmppath)

            assert len(files) == 3
            file_names = {f.name for f in files}
            assert file_names == {"main.py", "utils.py", "module.py"}

    def test_get_files_to_scan_with_exclude(self):
        """Test get_files_to_scan with exclude patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "main.py").write_text("# main")
            (tmppath / "test_main.py").write_text("# test")
            (tmppath / "utils.py").write_text("# utils")

            scanner = ConcreteTestScanner(
                include_patterns=["**/*.py"],
                exclude_patterns=["**/test_*.py"],
            )
            files = scanner.get_files_to_scan(tmppath)

            assert len(files) == 2
            file_names = {f.name for f in files}
            assert file_names == {"main.py", "utils.py"}

    def test_get_files_to_scan_multiple_include_patterns(self):
        """Test get_files_to_scan with multiple include patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "main.py").write_text("# main")
            (tmppath / "types.pyi").write_text("# types")
            (tmppath / "readme.md").write_text("# readme")

            scanner = ConcreteTestScanner(include_patterns=["**/*.py", "**/*.pyi"])
            files = scanner.get_files_to_scan(tmppath)

            assert len(files) == 2
            file_names = {f.name for f in files}
            assert file_names == {"main.py", "types.pyi"}

    def test_scan_integration(self):
        """Test full scan integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "main.py").write_text("# main")
            (tmppath / "utils.py").write_text("# utils")
            (tmppath / "test_main.py").write_text("# test")

            scanner = ConcreteTestScanner(
                include_patterns=["**/*.py"],
                exclude_patterns=["**/test_*.py"],
            )
            output = scanner.scan(tmppath)

            assert output.summary.total_count == 2
            assert output.summary.files_scanned == 2
            assert len(output.results) == 2


class TestParseFile:
    """Test parse_file method."""

    def test_parses_valid_python_file(self):
        """Test that parse_file successfully parses valid Python code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("x = 42\ndef foo(): pass")

            scanner = ConcreteTestScanner()
            module = scanner.parse_file(test_file)

            assert module is not None
            assert len(module.body) == 2

    def test_returns_none_for_nonexistent_file(self):
        """Test that parse_file returns None for nonexistent file."""
        scanner = ConcreteTestScanner()
        module = scanner.parse_file(Path("/nonexistent/file.py"))
        assert module is None

    def test_returns_none_for_syntax_error(self):
        """Test that parse_file returns None for file with syntax errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "bad.py"
            test_file.write_text("def foo(\n")  # Invalid syntax

            scanner = ConcreteTestScanner()
            module = scanner.parse_file(test_file)
            assert module is None

    def test_returns_none_for_encoding_error(self):
        """Test that parse_file returns None for encoding errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "bad_encoding.py"
            # Write invalid UTF-8 bytes
            test_file.write_bytes(b"\xff\xfe")

            scanner = ConcreteTestScanner()
            module = scanner.parse_file(test_file)
            assert module is None

    def test_verbose_mode_logs_errors(self):
        """Test that verbose mode logs parsing errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "bad.py"
            test_file.write_text("def foo(\n")

            scanner = ConcreteTestScanner(verbose=True)
            module = scanner.parse_file(test_file)
            assert module is None  # Should still return None

    def test_parses_empty_file(self):
        """Test that parse_file handles empty files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "empty.py"
            test_file.write_text("")

            scanner = ConcreteTestScanner()
            module = scanner.parse_file(test_file)

            assert module is not None
            assert len(module.body) == 0
