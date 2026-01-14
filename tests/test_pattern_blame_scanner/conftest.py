"""Fixtures for pattern blame scanner tests."""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def test_repo(tmp_path):
    """Create a temporary git repository with test files."""
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()

    # Initialize git repo
    import subprocess

    subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_dir,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        capture_output=True,
        check=True,
    )

    # Create test file
    test_file = repo_dir / "test.py"
    test_file.write_text(
        """import time
from pathlib import Path

def hello():
    print("Hello, world!")
"""
    )

    # Commit the file
    subprocess.run(["git", "add", "."], cwd=repo_dir, capture_output=True, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=repo_dir,
        capture_output=True,
        check=True,
    )

    return repo_dir


@pytest.fixture
def scanner():
    """Create a PatternBlameScanner instance."""
    from upcast.scanners.pattern_blame import PatternBlameScanner

    return PatternBlameScanner(
        patterns=["import time"],
        lang="python",
    )
