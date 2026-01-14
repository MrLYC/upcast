"""Tests for pattern blame Pydantic models."""

import pytest

from upcast.models.pattern_blame import (
    BlameHistory,
    CommitInfo,
    PatternBlameOutput,
    PatternBlameSummary,
    PatternMatch,
)


class TestCommitInfo:
    """Test CommitInfo model."""

    def test_basic_commit(self) -> None:
        """Test creating basic commit info."""
        commit = CommitInfo(
            commit_hash="abc1234",
            full_hash="abc1234567890abcdef",
            author="John Doe",
            author_email="john@example.com",
            date="2025-01-13T12:00:00",
            commit_message="Add new feature",
        )
        assert commit.commit_hash == "abc1234"
        assert commit.author == "John Doe"
        assert commit.commit_message == "Add new feature"


class TestBlameHistory:
    """Test BlameHistory model."""

    def test_basic_history(self) -> None:
        """Test creating basic blame history."""
        commit1 = CommitInfo(
            commit_hash="abc1234",
            full_hash="abc1234567890abcdef",
            author="Alice",
            author_email="alice@example.com",
            date="2025-01-13T10:00:00",
            commit_message="Initial commit",
        )
        commit2 = CommitInfo(
            commit_hash="def5678",
            full_hash="def567890123456789",
            author="Bob",
            author_email="bob@example.com",
            date="2025-01-13T11:00:00",
            commit_message="Update code",
        )

        history = BlameHistory(
            line=42,
            history=[commit1, commit2],
            latest_commit=commit2,
            original_commit=commit1,
            total_commits=2,
            total_authors=2,
        )
        assert history.line == 42
        assert history.total_commits == 2
        assert history.total_authors == 2
        assert len(history.history) == 2

    def test_single_commit_history(self) -> None:
        """Test history with single commit."""
        commit = CommitInfo(
            commit_hash="abc1234",
            full_hash="abc1234567890abcdef",
            author="Alice",
            author_email="alice@example.com",
            date="2025-01-13T10:00:00",
            commit_message="Initial commit",
        )

        history = BlameHistory(
            line=10,
            history=[commit],
            latest_commit=commit,
            original_commit=commit,
            total_commits=1,
            total_authors=1,
        )
        assert history.total_commits == 1
        assert history.total_authors == 1


class TestPatternMatch:
    """Test PatternMatch model."""

    def test_basic_match(self) -> None:
        """Test creating basic pattern match."""
        commit = CommitInfo(
            commit_hash="abc1234",
            full_hash="abc1234567890abcdef",
            author="Alice",
            author_email="alice@example.com",
            date="2025-01-13T10:00:00",
            commit_message="Initial commit",
        )
        history = BlameHistory(
            line=10,
            history=[commit],
            latest_commit=commit,
            original_commit=commit,
            total_commits=1,
            total_authors=1,
        )

        match = PatternMatch(
            file="test.py",
            line=10,
            pattern="import time",
            statement="import time",
            blame_history=history,
        )
        assert match.file == "test.py"
        assert match.line == 10
        assert match.pattern == "import time"


class TestPatternBlameSummary:
    """Test PatternBlameSummary model."""

    def test_basic_summary(self) -> None:
        """Test creating basic summary."""
        summary = PatternBlameSummary(
            total_count=10,
            files_scanned=5,
            patterns_matched=2,
            unique_commits=5,
            by_author={"Alice": 6, "Bob": 4},
        )
        assert summary.total_count == 10
        assert summary.patterns_matched == 2
        assert summary.unique_commits == 5
        assert summary.by_author["Alice"] == 6


class TestPatternBlameOutput:
    """Test PatternBlameOutput model."""

    def test_basic_output(self) -> None:
        """Test creating basic output."""
        summary = PatternBlameSummary(
            total_count=1,
            files_scanned=1,
            patterns_matched=1,
            unique_commits=1,
            by_author={"Alice": 1},
        )

        commit = CommitInfo(
            commit_hash="abc1234",
            full_hash="abc1234567890abcdef",
            author="Alice",
            author_email="alice@example.com",
            date="2025-01-13T10:00:00",
            commit_message="Initial commit",
        )
        history = BlameHistory(
            line=10,
            history=[commit],
            latest_commit=commit,
            original_commit=commit,
            total_commits=1,
            total_authors=1,
        )
        match = PatternMatch(
            file="test.py",
            line=10,
            pattern="import time",
            statement="import time",
            blame_history=history,
        )

        output = PatternBlameOutput(
            summary=summary,
            results={"import time": [match]},
        )
        assert output.summary.total_count == 1
        assert len(output.results) == 1
        assert "import time" in output.results
