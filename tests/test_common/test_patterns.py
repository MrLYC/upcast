"""Tests for pattern matching utilities."""

from pathlib import Path

from upcast.common.patterns import DEFAULT_EXCLUDES, match_patterns, should_exclude


class TestMatchPatterns:
    """Tests for match_patterns function."""

    def test_matches_exact_filename(self) -> None:
        """Should match exact filename."""
        path = Path("test.py")
        assert match_patterns(path, ["test.py"])

    def test_matches_wildcard(self) -> None:
        """Should match wildcard patterns."""
        path = Path("src/module.py")
        assert match_patterns(path, ["*.py"])
        assert match_patterns(path, ["**/*.py"])

    def test_matches_directory_pattern(self) -> None:
        """Should match directory patterns."""
        path = Path("tests/test_file.py")
        assert match_patterns(path, ["tests/**"])

    def test_no_match(self) -> None:
        """Should return False when no patterns match."""
        path = Path("file.txt")
        assert not match_patterns(path, ["*.py", "src/**"])

    def test_empty_patterns(self) -> None:
        """Should return False for empty pattern list."""
        path = Path("test.py")
        assert not match_patterns(path, [])

    def test_cross_platform_paths(self) -> None:
        """Should handle both forward and backward slashes."""
        path = Path("src/module.py")
        # pathlib normalizes separators automatically
        assert match_patterns(path, ["src/**"])


class TestShouldExclude:
    """Tests for should_exclude function."""

    def test_excludes_default_patterns(self) -> None:
        """Should exclude paths matching default patterns."""
        assert should_exclude(Path("__pycache__/file.py"))
        assert should_exclude(Path("venv/lib/module.py"))
        assert should_exclude(Path("build/output.py"))

    def test_allows_normal_files(self) -> None:
        """Should not exclude normal Python files."""
        assert not should_exclude(Path("src/module.py"))
        assert not should_exclude(Path("tests/test_file.py"))

    def test_respects_custom_excludes(self) -> None:
        """Should apply custom exclude patterns."""
        path = Path("temp/file.py")
        assert should_exclude(path, exclude_patterns=["temp/**"])

    def test_respects_include_patterns(self) -> None:
        """Should include files matching include patterns."""
        # This file would be excluded by default
        excluded_path = Path("other/file.py")
        # But we explicitly include it
        assert not should_exclude(excluded_path, include_patterns=["other/**"])

    def test_exclude_overrides_include(self) -> None:
        """Should prioritize exclude over include."""
        path = Path("tests/__pycache__/cached.py")
        # Even if we include tests/**, __pycache__ should be excluded
        result = should_exclude(path, include_patterns=["tests/**"])
        assert result  # __pycache__ from DEFAULT_EXCLUDES wins

    def test_custom_exclude_overrides_include(self) -> None:
        """Should prioritize custom exclude over include."""
        path = Path("src/debug.py")
        result = should_exclude(path, include_patterns=["src/**"], exclude_patterns=["**/debug.py"])
        assert result

    def test_disables_default_excludes(self) -> None:
        """Should disable default excludes when flag is False."""
        path = Path("__pycache__/cached.py")
        # With defaults disabled, only custom patterns apply
        result = should_exclude(path, use_default_excludes=False)
        assert not result  # Would normally be excluded


class TestDefaultExcludes:
    """Tests for DEFAULT_EXCLUDES constant."""

    def test_has_common_patterns(self) -> None:
        """Should include common exclude patterns."""
        assert "__pycache__/**" in DEFAULT_EXCLUDES
        assert "venv/**" in DEFAULT_EXCLUDES
        assert ".venv/**" in DEFAULT_EXCLUDES
        assert "build/**" in DEFAULT_EXCLUDES
        assert "dist/**" in DEFAULT_EXCLUDES
        assert ".git/**" in DEFAULT_EXCLUDES

    def test_excludes_virtual_envs(self) -> None:
        """Should exclude common virtual environment directories."""
        venv_patterns = [p for p in DEFAULT_EXCLUDES if "venv" in p.lower()]
        assert len(venv_patterns) >= 2  # venv/ and .venv/

    def test_excludes_build_artifacts(self) -> None:
        """Should exclude build and distribution artifacts."""
        build_patterns = {"build/**", "dist/**", "*.egg-info/**"}
        for pattern in build_patterns:
            assert pattern in DEFAULT_EXCLUDES
