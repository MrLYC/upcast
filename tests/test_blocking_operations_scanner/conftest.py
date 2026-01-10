"""Pytest fixtures for blocking_operations scanner tests."""

import pytest
from pathlib import Path

from upcast.scanners.blocking_operations import BlockingOperationsScanner
from tests.test_blocking_operations_scanner.fixtures import (
    time_based_ops,
    synchronization_ops,
    subprocess_ops,
    database_ops,
    mixed_contexts,
)


@pytest.fixture
def scanner():
    """Create a BlockingOperationsScanner instance."""
    return BlockingOperationsScanner(verbose=False)


@pytest.fixture
def fixtures_dir():
    """Get the fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def time_based_fixtures():
    """Time-based blocking operations fixtures as dict."""
    return {
        "TIME_SLEEP": """
import time

def delayed():
    time.sleep(1)
""",
        "ASYNCIO_SLEEP": """
import asyncio

async def async_delayed():
    await asyncio.sleep(1)
""",
    }


@pytest.fixture
def sync_fixtures():
    """Synchronization fixtures as dict."""
    return {
        "THREADING_LOCK": """
import threading

def use_lock():
    lock = threading.Lock()
""",
        "THREADING_SEMAPHORE": """
import threading

def use_semaphore():
    sem = threading.Semaphore()
""",
    }


@pytest.fixture
def subprocess_fixtures():
    """Subprocess fixtures as dict."""
    return {
        "SUBPROCESS_RUN": """
import subprocess

def run_command():
    subprocess.run(['ls'])
""",
        "SUBPROCESS_CALL": """
import subprocess

def call_command():
    subprocess.call(['echo', 'test'])
""",
    }


@pytest.fixture
def database_fixtures():
    """Database fixtures as dict."""
    return {
        "SELECT_FOR_UPDATE": """
def lock_row(queryset):
    queryset.select_for_update()
""",
        "DJANGO_TRANSACTION": """
from django.db import transaction

def atomic_operation():
    with transaction.atomic():
        pass
""",
    }
