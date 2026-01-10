"""Test utilities for scanner testing."""

from pathlib import Path
from typing import Any, Dict


def assert_valid_summary(summary: Any, required_fields: list[str]) -> None:
    """
    Assert that a summary object has all required fields.

    Args:
        summary: Summary object to validate
        required_fields: List of required field names
    """
    for field in required_fields:
        assert hasattr(summary, field), f"Summary missing required field: {field}"


def assert_valid_metadata(metadata: Dict, scanner_name: str) -> None:
    """
    Assert that metadata is valid.

    Args:
        metadata: Metadata dict to validate
        scanner_name: Expected scanner name
    """
    assert "scanner_name" in metadata
    assert metadata["scanner_name"] == scanner_name


def create_test_file(tmp_path: Path, content: str, filename: str = "test.py") -> Path:
    """
    Create a test Python file with given content.

    Args:
        tmp_path: Temporary directory path
        content: File content
        filename: File name (default: test.py)

    Returns:
        Path to created file
    """
    file_path = tmp_path / filename
    file_path.write_text(content)
    return file_path


def create_test_project(tmp_path: Path, structure: Dict[str, str]) -> Path:
    """
    Create a test project with multiple files.

    Args:
        tmp_path: Temporary directory path
        structure: Dict mapping relative paths to content

    Returns:
        Path to project root
    """
    for rel_path, content in structure.items():
        file_path = tmp_path / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    return tmp_path


def assert_scanner_output_valid(output: Any, expected_scanner_name: str) -> None:
    """
    Assert that scanner output structure is valid.

    Args:
        output: Scanner output object
        expected_scanner_name: Expected scanner name in metadata
    """
    # Check metadata
    assert hasattr(output, "metadata")
    assert "scanner_name" in output.metadata
    assert output.metadata["scanner_name"] == expected_scanner_name

    # Check summary
    assert hasattr(output, "summary")
    assert hasattr(output.summary, "total_count")
    assert hasattr(output.summary, "files_scanned")
    assert hasattr(output.summary, "scan_duration_ms")

    # Check results
    assert hasattr(output, "results")


def count_patterns_in_results(results: Any, pattern_type: str = None) -> int:
    """
    Count total patterns in results.

    Args:
        results: Results object (dict, list, or custom type)
        pattern_type: Optional pattern type to filter by

    Returns:
        Count of patterns
    """
    if isinstance(results, dict):
        total = 0
        for key, value in results.items():
            if pattern_type and key != pattern_type:
                continue
            if isinstance(value, list):
                total += len(value)
            elif isinstance(value, dict):
                total += sum(len(v) if isinstance(v, list) else 1 for v in value.values())
        return total
    elif isinstance(results, list):
        return len(results)
    else:
        return 0
