"""Shared pytest fixtures for all scanner tests."""

import pytest
import tempfile
from pathlib import Path
from typing import Callable, Dict


@pytest.fixture
def tmp_py_file(tmp_path: Path) -> Callable:
    """
    Create a temporary Python file.

    Returns a function that creates a file with given content.

    Example:
        def test_something(tmp_py_file):
            file_path = tmp_py_file('print("hello")', 'test.py')
            # Use file_path...
    """

    def _create(content: str, filename: str = "test.py") -> Path:
        file_path = tmp_path / filename
        file_path.write_text(content)
        return file_path

    return _create


@pytest.fixture
def tmp_project(tmp_path: Path) -> Callable:
    """
    Create a temporary project structure.

    Returns a function that creates multiple files from a dict structure.

    Example:
        def test_something(tmp_project):
            project_dir = tmp_project({
                "app/models.py": "class Model: pass",
                "app/views.py": "def view(): pass",
            })
            # Use project_dir...
    """

    def _create(structure: Dict[str, str]) -> Path:
        """
        Create project structure from dict.

        Args:
            structure: Dict mapping file paths to file contents
                      e.g., {"app/models.py": "...code..."}

        Returns:
            Path to the created project directory
        """
        for path, content in structure.items():
            file_path = tmp_path / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        return tmp_path

    return _create


@pytest.fixture
def scanner_kwargs() -> Dict:
    """
    Default scanner initialization kwargs.

    Returns:
        Dict with default scanner parameters
    """
    return {
        "verbose": False,
        "include_patterns": ["**/*.py"],
        "exclude_patterns": [],
    }


@pytest.fixture
def create_scanner():
    """
    Factory fixture for creating scanner instances.

    Example:
        def test_something(create_scanner):
            from upcast.scanners.env_vars import EnvVarScanner
            scanner = create_scanner(EnvVarScanner)
            # Use scanner...
    """

    def _factory(scanner_class, **kwargs):
        """Create a scanner instance with given kwargs."""
        return scanner_class(**kwargs)

    return _factory
