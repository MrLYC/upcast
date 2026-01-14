"""Data models for pattern blame scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class CommitInfo(BaseModel):
    """Information about a single commit.

    Attributes:
        commit_hash: Short commit hash (7 chars)
        full_hash: Full commit hash
        author: Author name
        author_email: Author email
        date: Commit date (ISO format)
        commit_message: Commit message subject
    """

    commit_hash: str = Field(description="Short commit hash")
    full_hash: str = Field(description="Full commit hash")
    author: str = Field(description="Author name")
    author_email: str = Field(description="Author email")
    date: str = Field(description="Commit date (ISO format)")
    commit_message: str = Field(description="Commit message subject")


class BlameHistory(BaseModel):
    """Complete git history for a matched line.

    Attributes:
        line: Line number in the file
        history: List of commits that modified this line (oldest to newest)
        latest_commit: Most recent commit
        original_commit: First commit that introduced this line
        total_commits: Total number of commits
        total_authors: Number of unique authors
    """

    line: int = Field(ge=1, description="Line number")
    history: list[CommitInfo] = Field(description="Commit history (oldest to newest)")
    latest_commit: CommitInfo = Field(description="Most recent commit")
    original_commit: CommitInfo = Field(description="First commit")
    total_commits: int = Field(ge=1, description="Total commits")
    total_authors: int = Field(ge=1, description="Unique authors count")


class PatternMatch(BaseModel):
    """A single pattern match with its blame history.

    Attributes:
        file: File path (relative to scan root)
        line: Line number where pattern was matched
        pattern: The ast-grep pattern that matched
        statement: The actual code statement that matched
        blame_history: Complete git history for this match
    """

    file: str = Field(description="File path")
    line: int = Field(ge=1, description="Line number")
    pattern: str = Field(description="Pattern that matched")
    statement: str = Field(description="Matched code statement")
    blame_history: BlameHistory = Field(description="Git history")


class PatternBlameSummary(ScannerSummary):
    """Summary statistics for pattern blame scan.

    Attributes:
        patterns_matched: Number of different patterns that had matches
        unique_commits: Total unique commits across all matches
        by_author: Number of matches per author
    """

    patterns_matched: int = Field(ge=0, description="Number of patterns matched")
    unique_commits: int = Field(ge=0, description="Unique commits")
    by_author: dict[str, int] = Field(default_factory=dict, description="Matches per author")


class PatternBlameOutput(ScannerOutput[dict[str, list[PatternMatch]]]):
    """Complete output from pattern blame scanner.

    Results are grouped by pattern, with each pattern having a list of matches.

    Attributes:
        summary: Summary statistics
        results: Matches grouped by pattern
    """

    summary: PatternBlameSummary
    results: dict[str, list[PatternMatch]] = Field(description="Matches by pattern")
