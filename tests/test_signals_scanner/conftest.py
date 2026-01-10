"""Fixtures for signals scanner tests."""

import pytest


@pytest.fixture
def scanner():
    """Create a SignalScanner instance."""
    from upcast.scanners.signals import SignalScanner

    return SignalScanner()
