"""Fixtures for Django settings scanner tests."""

from pathlib import Path

import pytest


@pytest.fixture
def scanner():
    """Create a DjangoSettingsScanner instance."""
    from upcast.scanners.django_settings import DjangoSettingsScanner

    return DjangoSettingsScanner()
