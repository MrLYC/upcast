"""Pattern blame scanner with git history tracking."""

import logging
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.pattern_blame import (
    BlameHistory,
    CommitInfo,
    PatternBlameOutput,
    PatternBlameSummary,
    PatternMatch,
)

logger = logging.getLogger(__name__)

LANGUAGE_MAP = {
    "py": "python",
    "python": "python",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "tsx": "tsx",
    "jsx": "javascript",
    "go": "go",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "cs": "csharp",
    "csharp": "csharp",
    "rb": "ruby",
    "ruby": "ruby",
    "rs": "rust",
    "rust": "rust",
}


class PatternBlameScanner(BaseScanner[PatternBlameOutput]):
    """Scanner that combines ast-grep pattern matching with git blame history."""

    def __init__(
        self,
        patterns: list[str] | None = None,
        pattern_file: Path | None = None,
        lang: str | None = None,
        max_history_depth: int = 50,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize pattern blame scanner.

        Args:
            patterns: List of ast-grep patterns to search
            pattern_file: File containing patterns (one per line)
            lang: Language code (python, ts, js, go, etc.)
            max_history_depth: Maximum number of commits to track per line
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose logging
        """
        super().__init__(include_patterns, exclude_patterns, verbose)
        self.patterns = patterns or []
        self.pattern_file = pattern_file
        self.lang = self._normalize_language(lang) if lang else None
        self.max_history_depth = max_history_depth
        self.base_path: Path | None = None

        if pattern_file:
            self._load_patterns_from_file()

        if not self.patterns:
            msg = "At least one pattern must be provided via --pattern or --pattern-file"
            raise ValueError(msg)

    def _normalize_language(self, lang: str) -> str:
        """Normalize language code to ast-grep format."""
        lang_lower = lang.lower()
        return LANGUAGE_MAP.get(lang_lower, lang_lower)

    def _load_patterns_from_file(self) -> None:
        """Load patterns from file, skipping empty lines and comments."""
        if not self.pattern_file or not self.pattern_file.exists():
            return

        with open(self.pattern_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    self.patterns.append(line)

    def scan(self, path: Path) -> PatternBlameOutput:
        """Scan path for patterns and collect git history."""
        start_time = time.time()
        self.base_path = path.resolve() if path.is_dir() else path.parent.resolve()

        if not self._is_git_repository():
            msg = f"Not a git repository: {self.base_path}"
            raise RuntimeError(msg)

        all_matches, files_scanned = self._scan_all_patterns(path)

        summary = self._calculate_summary(
            all_matches=all_matches,
            files_scanned=files_scanned,
            scan_duration_ms=int((time.time() - start_time) * 1000),
        )

        return PatternBlameOutput(
            summary=summary,
            results=dict(all_matches),
            metadata={"scanner_name": "pattern-blame"},
        )

    def _is_git_repository(self) -> bool:
        """Check if path is inside a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.base_path,
                capture_output=True,
                timeout=5,
                check=False,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _scan_all_patterns(self, path: Path) -> tuple[dict[str, list[PatternMatch]], int]:
        """Scan all files for all patterns in a single pass using ast-grep 'any' rule."""
        all_matches: dict[str, list[PatternMatch]] = defaultdict(list)
        files_with_matches: set[str] = set()

        try:
            from ast_grep_py import SgRoot
        except ImportError:
            logger.error("ast-grep-py is not installed. Run: pip install ast-grep-py")
            return all_matches, 0

        files = self.get_files_to_scan(path)
        if not files:
            return all_matches, 0

        lang = self.lang or self._detect_language_from_files(files)
        if not lang:
            logger.warning("Could not detect language. Use --lang flag.")
            return all_matches, 0

        any_rules = [{"pattern": p} for p in self.patterns]

        for file_path in files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                root = SgRoot(content, lang)
                node = root.root()
                file_matches = node.find_all(any=any_rules)

                for match in file_matches:
                    line_num = match.range().start.line + 1
                    statement = match.text()

                    matched_pattern = self._identify_pattern(match)
                    if not matched_pattern:
                        continue

                    blame_history = self._get_complete_git_history(file_path, line_num)
                    if not blame_history:
                        continue

                    relative_path = get_relative_path_str(file_path, self.base_path or Path.cwd())
                    files_with_matches.add(relative_path)

                    pattern_match = PatternMatch(
                        file=relative_path,
                        line=line_num,
                        pattern=matched_pattern,
                        statement=statement,
                        blame_history=blame_history,
                    )
                    all_matches[matched_pattern].append(pattern_match)

            except Exception as e:
                if self.verbose:
                    logger.warning("Failed to scan %s: %s", file_path, e)

        return all_matches, len(files_with_matches)

    def _identify_pattern(self, match) -> str | None:  # noqa: ANN001
        """Find which pattern from self.patterns matches the given node."""
        for pattern in self.patterns:
            if match.matches(pattern=pattern):
                return pattern
        return None

    def _detect_language_from_files(self, files: list[Path]) -> str | None:
        """Auto-detect language from file extensions."""
        if not files:
            return None

        first_file = files[0]
        ext = first_file.suffix.lstrip(".")
        return LANGUAGE_MAP.get(ext)

    def _get_complete_git_history(self, file_path: Path, line: int) -> BlameHistory | None:
        """Get complete git history for a specific line using git log -L."""
        try:
            relative_path = get_relative_path_str(file_path, self.base_path or Path.cwd())

            cmd = [
                "git",
                "log",
                f"-L{line},{line}:{relative_path}",
                "--format=%H|%h|%an|%ae|%ai|%s",
                "--reverse",
            ]

            result = subprocess.run(
                cmd,
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode != 0:
                if self.verbose:
                    logger.warning("git log failed for %s:%d - %s", file_path, line, result.stderr)
                return None

            commits = self._parse_git_log_output(result.stdout)
            if not commits:
                return None

            commits = commits[: self.max_history_depth]

            unique_authors = len({c.author for c in commits})

            return BlameHistory(
                line=line,
                history=commits,
                latest_commit=commits[-1],
                original_commit=commits[0],
                total_commits=len(commits),
                total_authors=unique_authors,
            )

        except subprocess.TimeoutExpired:
            if self.verbose:
                logger.warning("git log timed out for %s:%d", file_path, line)
            return None
        except Exception as e:
            if self.verbose:
                logger.warning("Failed to get git history for %s:%d - %s", file_path, line, e)
            return None

    def _parse_git_log_output(self, output: str) -> list[CommitInfo]:
        """Parse git log output into CommitInfo objects."""
        commits: list[CommitInfo] = []
        pattern = re.compile(r"^([0-9a-fA-F]+)\|([0-9a-fA-F]+)\|(.*?)\|(.*?)\|(.*?)\|(.*)$", re.MULTILINE)

        for match in pattern.finditer(output):
            full_hash, commit_hash, author, email, date, message = match.groups()
            commits.append(
                CommitInfo(
                    commit_hash=commit_hash,
                    full_hash=full_hash,
                    author=author,
                    author_email=email,
                    date=date,
                    commit_message=message,
                )
            )

        return commits

    def _calculate_summary(
        self,
        all_matches: dict[str, list[PatternMatch]],
        files_scanned: int,
        scan_duration_ms: int,
    ) -> PatternBlameSummary:
        """Calculate summary statistics."""
        total_matches = sum(len(matches) for matches in all_matches.values())
        patterns_matched = len(all_matches)

        unique_commits: set[str] = set()
        author_counts: dict[str, int] = defaultdict(int)

        for matches in all_matches.values():
            for match in matches:
                for commit in match.blame_history.history:
                    unique_commits.add(commit.full_hash)
                    author_counts[match.blame_history.latest_commit.author] += 1

        return PatternBlameSummary(
            total_count=total_matches,
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            patterns_matched=patterns_matched,
            unique_commits=len(unique_commits),
            by_author=dict(author_counts),
        )
