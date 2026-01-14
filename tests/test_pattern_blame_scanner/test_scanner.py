"""Tests for pattern blame scanner functionality."""

import pytest

from upcast.models.pattern_blame import PatternBlameSummary
from upcast.scanners.pattern_blame import PatternBlameScanner


class TestLanguageNormalization:
    """Test language code normalization."""

    @pytest.fixture
    def scanner(self):
        """Create scanner instance."""
        return PatternBlameScanner(
            patterns=["import time"],
        )

    def test_python_normalization(self, scanner) -> None:
        """Test Python language normalization."""
        assert scanner._normalize_language("python") == "python"
        assert scanner._normalize_language("py") == "python"

    def test_typescript_normalization(self, scanner) -> None:
        """Test TypeScript language normalization."""
        assert scanner._normalize_language("typescript") == "typescript"
        assert scanner._normalize_language("ts") == "typescript"
        assert scanner._normalize_language("tsx") == "tsx"

    def test_javascript_normalization(self, scanner) -> None:
        """Test JavaScript language normalization."""
        assert scanner._normalize_language("javascript") == "javascript"
        assert scanner._normalize_language("js") == "javascript"
        assert scanner._normalize_language("jsx") == "javascript"

    def test_case_insensitive(self, scanner) -> None:
        """Test case-insensitive normalization."""
        assert scanner._normalize_language("Python") == "python"
        assert scanner._normalize_language("JS") == "javascript"


class TestPatternFileLoading:
    """Test pattern file loading."""

    def test_load_patterns_from_file(self, tmp_path) -> None:
        """Test loading patterns from file."""
        import tempfile

        pattern_file = tmp_path / "patterns.txt"
        pattern_file.write_text(
            """# This is a comment
import time
from pathlib import Path

# Another comment
logger.$_($$$)
"""
        )

        scanner = PatternBlameScanner(pattern_file=pattern_file)
        assert "import time" in scanner.patterns
        assert "from pathlib import Path" in scanner.patterns
        assert "logger.$_($$$)" in scanner.patterns
        assert len(scanner.patterns) == 3

    def test_skip_empty_lines(self, tmp_path) -> None:
        """Test skipping empty lines in pattern file."""
        pattern_file = tmp_path / "patterns.txt"
        pattern_file.write_text(
            """
import time

from pathlib import Path

"""
        )

        scanner = PatternBlameScanner(pattern_file=pattern_file)
        assert len(scanner.patterns) == 2

    def test_no_pattern_file(self, tmp_path) -> None:
        """Test scanner without pattern file."""
        scanner = PatternBlameScanner(
            patterns=["import time", "from pathlib import Path"],
        )
        assert len(scanner.patterns) == 2

    def test_nonexistent_pattern_file(self, tmp_path) -> None:
        """Test scanner with non-existent pattern file raises ValueError."""
        pattern_file = tmp_path / "nonexistent.txt"

        with pytest.raises(ValueError, match="At least one pattern"):
            PatternBlameScanner(pattern_file=pattern_file)


class TestGitLogParsing:
    """Test git log output parsing."""

    def test_parse_single_commit(self) -> None:
        """Test parsing single commit."""
        output = """abc1234567890abcdef|abc1234|John Doe|john@example.com|2025-01-13 12:00:00 +0800|Add feature"""

        scanner = PatternBlameScanner(patterns=["import time"])
        commits = scanner._parse_git_log_output(output)

        assert len(commits) == 1
        assert commits[0].commit_hash == "abc1234"
        assert commits[0].full_hash == "abc1234567890abcdef"
        assert commits[0].author == "John Doe"
        assert commits[0].author_email == "john@example.com"
        assert commits[0].commit_message == "Add feature"

    def test_parse_multiple_commits(self) -> None:
        """Test parsing multiple commits."""
        from pathlib import Path

        output_path = Path("/tmp/test_git_log3.txt")
        with open(output_path, "w") as f:
            f.write("abc1234567890abcdef|abc1234|Alice|alice@example.com|2025-01-13 10:00:00 +0800|Initial commit\n")
            f.write(
                "def5678901234567890123456789abcdef|def5678|Bob|bob@example.com|2025-01-13 11:00:00 +0800|Update code\n"
            )

        output = output_path.read_text()
        scanner = PatternBlameScanner(patterns=["import time"])
        commits = scanner._parse_git_log_output(output)

        assert len(commits) == 2
        assert commits[0].author == "Alice"
        assert commits[1].author == "Bob"

    def test_parse_empty_output(self) -> None:
        """Test parsing empty output."""
        output = ""

        scanner = PatternBlameScanner(patterns=["import time"])
        commits = scanner._parse_git_log_output(output)

        assert len(commits) == 0


class TestScannerIntegration:
    """Test scanner integration with temporary git repo."""

    def test_scan_with_git_history(self, test_repo) -> None:
        """Test scanning a git repository with history."""
        scanner = PatternBlameScanner(
            patterns=["import time"],
            lang="python",
        )

        result = scanner.scan(test_repo)

        assert isinstance(result.summary, PatternBlameSummary)
        assert result.summary.total_count >= 0
        assert result.metadata["scanner_name"] == "pattern-blame"

    def test_scan_with_language_specification(self, test_repo) -> None:
        """Test scanning with explicit language."""
        scanner = PatternBlameScanner(
            patterns=["from pathlib import Path"],
            lang="python",
        )

        result = scanner.scan(test_repo)

        assert isinstance(result.summary, PatternBlameSummary)
        assert "from pathlib import Path" in result.results

    def test_scan_with_multiple_patterns(self, test_repo) -> None:
        """Test scanning with multiple patterns."""
        scanner = PatternBlameScanner(
            patterns=["import time", "from pathlib import Path"],
            lang="python",
        )

        result = scanner.scan(test_repo)

        assert result.summary.patterns_matched >= 1
        assert len(result.results) >= 1

    def test_scan_without_git_repo(self, tmp_path) -> None:
        """Test scanning a directory without git repository."""
        non_git_dir = tmp_path / "non_git"
        non_git_dir.mkdir()

        # Create a file without git
        test_file = non_git_dir / "test.py"
        test_file.write_text("import time")

        scanner = PatternBlameScanner(
            patterns=["import time"],
            lang="python",
        )

        with pytest.raises(RuntimeError, match="Not a git repository"):
            scanner.scan(non_git_dir)

    def test_max_history_depth(self, test_repo) -> None:
        """Test max history depth limitation."""
        scanner = PatternBlameScanner(
            patterns=["import time"],
            lang="python",
            max_history_depth=5,
        )

        result = scanner.scan(test_repo)

        for matches in result.results.values():
            for match in matches:
                assert match.blame_history.total_commits <= 5

    def test_verbose_mode_logs_exceptions(self, test_repo) -> None:
        """Test verbose mode logs exceptions during scanning."""
        import subprocess
        from unittest.mock import patch

        scanner = PatternBlameScanner(
            patterns=["some_pattern_that_does_not_exist_xyz"],
            lang="python",
            verbose=True,
        )

        original_run = subprocess.run

        def selective_timeout(*args, **kwargs):
            if "-L" in args[0]:
                raise subprocess.TimeoutExpired("git", 5)
            return original_run(*args, **kwargs)

        with patch.object(subprocess, "run", side_effect=selective_timeout):
            result = scanner.scan(test_repo)
            assert result.summary.total_count == 0

    def test_git_log_failure_verbose(self) -> None:
        """Test git log failure with verbose logging."""
        import subprocess
        from pathlib import Path
        from unittest.mock import patch

        scanner = PatternBlameScanner(
            patterns=["import time"],
            lang="python",
            verbose=True,
        )

        result = subprocess.CompletedProcess(args=[], returncode=1, stderr="git log error", stdout="")

        with patch.object(subprocess, "run", return_value=result):
            blame = scanner._get_complete_git_history(Path("test.py"), 5)
            assert blame is None

    def test_language_detection_failure(self, tmp_path) -> None:
        """Test scanner fails when language cannot be detected."""
        import tempfile
        import subprocess

        non_git_dir = tmp_path / "no_lang"
        non_git_dir.mkdir()

        subprocess.run(["git", "init"], cwd=non_git_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=non_git_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=non_git_dir, check=True)

        test_file = non_git_dir / "test.unknown"
        test_file.write_text("import time")

        subprocess.run(["git", "add", "."], cwd=non_git_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=non_git_dir, check=True)

        scanner = PatternBlameScanner(patterns=["import time"], verbose=True)
        result = scanner.scan(non_git_dir)
        assert result.summary.total_count == 0

    def test_empty_files(self, tmp_path) -> None:
        """Test scanner with no matching files."""
        import subprocess

        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        subprocess.run(["git", "init"], cwd=empty_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=empty_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=empty_dir, check=True)

        subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial"], cwd=empty_dir, check=True)

        scanner = PatternBlameScanner(patterns=["import time"], lang="python")
        result = scanner.scan(empty_dir)
        assert result.summary.total_count == 0

    def test_empty_git_log_output(self, tmp_path) -> None:
        """Test handling of empty git log output."""
        scanner = PatternBlameScanner(patterns=["import time"])
        commits = scanner._parse_git_log_output("")
        assert len(commits) == 0

    def test_identify_pattern_no_match(self) -> None:
        """Test _identify_pattern returns None when no pattern matches."""
        scanner = PatternBlameScanner(patterns=["import time"])
        from ast_grep_py import SgRoot

        code = "print('hello')"
        root = SgRoot(code, "python")
        node = root.root()
        matches = node.find_all(pattern="print($$$)")

        assert matches
        assert scanner._identify_pattern(matches[0]) is None

    def test_import_error_handling(self, tmp_path) -> None:
        """Test ImportError handling when ast-grep-py is not available."""
        import subprocess
        from unittest.mock import patch

        non_git_dir = tmp_path / "no_ast_grep"
        non_git_dir.mkdir()

        subprocess.run(["git", "init"], cwd=non_git_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=non_git_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=non_git_dir, check=True)

        test_file = non_git_dir / "test.py"
        test_file.write_text("import time")

        subprocess.run(["git", "add", "."], cwd=non_git_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=non_git_dir, check=True)

        with patch.dict("sys.modules", {"ast_grep_py": None}):
            scanner = PatternBlameScanner(patterns=["import time"], lang="python", verbose=True)
            result = scanner.scan(non_git_dir)
            assert result.summary.total_count == 0

    def test_file_io_exception(self, test_repo) -> None:
        """Test handling file scanning exceptions."""
        from unittest.mock import patch

        scanner = PatternBlameScanner(patterns=["import time"], lang="python", verbose=True)

        with patch("builtins.open", side_effect=IOError("Permission denied")):
            result = scanner.scan(test_repo)
            assert result.summary.total_count == 0

    def test_is_git_repo_timeout(self, tmp_path) -> None:
        """Test git repo check with timeout."""
        import subprocess
        from unittest.mock import patch

        test_dir = tmp_path / "timeout_test"
        test_dir.mkdir()

        scanner = PatternBlameScanner(patterns=["import time"], lang="python")

        with patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 5)):
            result = scanner._is_git_repository()
            assert result is False

    def test_is_git_repo_no_git(self, tmp_path) -> None:
        """Test git repo check when git is not available."""
        import subprocess
        from unittest.mock import patch, MagicMock

        test_dir = tmp_path / "no_git_test"
        test_dir.mkdir()

        scanner = PatternBlameScanner(patterns=["import time"], lang="python")

        with patch.object(subprocess, "run", side_effect=FileNotFoundError()):
            result = scanner._is_git_repository()
            assert result is False
