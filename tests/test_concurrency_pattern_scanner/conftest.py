"""Pytest fixtures for concurrency pattern scanner tests."""

import pytest
from pathlib import Path

from upcast.scanners.concurrency import ConcurrencyScanner


@pytest.fixture
def scanner():
    """Create a ConcurrencyScanner instance."""
    return ConcurrencyScanner(verbose=False)


@pytest.fixture
def fixtures_dir():
    """Get the fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def threading_fixtures():
    """Threading pattern fixtures as dict."""
    return {
        "THREAD_CREATION": """
import threading

def create_thread():
    t = threading.Thread(target=worker, name="worker-1")
    t.start()

def worker():
    pass
""",
        "THREADPOOL_EXECUTOR": """
from concurrent.futures import ThreadPoolExecutor

def use_threadpool():
    executor = ThreadPoolExecutor(max_workers=4)
    future = executor.submit(task)

def task():
    pass
""",
    }


@pytest.fixture
def multiprocessing_fixtures():
    """Multiprocessing pattern fixtures as dict."""
    return {
        "PROCESS_CREATION": """
import multiprocessing

def create_process():
    p = multiprocessing.Process(target=worker, name="process-1")
    p.start()

def worker():
    pass
""",
        "PROCESSPOOL_EXECUTOR": """
from concurrent.futures import ProcessPoolExecutor

def use_processpool():
    executor = ProcessPoolExecutor(max_workers=2)
    future = executor.submit(compute)

def compute():
    return 42
""",
    }


@pytest.fixture
def asyncio_fixtures():
    """Asyncio pattern fixtures as dict."""
    return {
        "ASYNC_FUNCTION": """
import asyncio

async def async_task():
    await asyncio.sleep(1)
    return "done"
""",
        "CREATE_TASK": """
import asyncio

async def create_tasks():
    task = asyncio.create_task(worker())
    await task

async def worker():
    pass
""",
        "AWAIT_EXPRESSION": """
import asyncio

async def await_example():
    result = await some_coroutine()
    return result

async def some_coroutine():
    return 42
""",
    }
