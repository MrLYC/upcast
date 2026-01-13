"""Fixtures for Django model scanner tests."""

from pathlib import Path

import pytest


@pytest.fixture
def scanner():
    """Create a DjangoModelScanner instance."""
    from upcast.scanners.django_models import DjangoModelScanner

    return DjangoModelScanner()
