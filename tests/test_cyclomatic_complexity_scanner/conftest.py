"""Pytest fixtures for complexity scanner tests."""

import pytest

from upcast.scanners.complexity import ComplexityScanner


@pytest.fixture
def scanner():
    """Create complexity scanner instance with default threshold."""
    return ComplexityScanner(threshold=11, verbose=False)


@pytest.fixture
def low_threshold_scanner():
    """Create complexity scanner instance with low threshold for testing."""
    return ComplexityScanner(threshold=1, verbose=False)


@pytest.fixture
def high_threshold_scanner():
    """Create complexity scanner instance with high threshold."""
    return ComplexityScanner(threshold=20, verbose=False)
