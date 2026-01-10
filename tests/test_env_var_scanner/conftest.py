"""Fixtures for environment variable scanner tests."""

import pytest


@pytest.fixture
def scanner():
    """Create an EnvVarScanner instance."""
    from upcast.scanners.env_vars import EnvVarScanner

    return EnvVarScanner()
