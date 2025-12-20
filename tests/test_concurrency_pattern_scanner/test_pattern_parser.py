"""Tests for pattern parser functions."""

from pathlib import Path

import pytest
from astroid import parse

from upcast.concurrency_pattern_scanner.pattern_parser import (
    parse_async_context_manager,
    parse_async_function,
    parse_asyncio_create_task,
    parse_asyncio_gather,
    parse_await_expression,
    parse_process_creation,
    parse_process_pool_executor,
    parse_run_in_executor,
    parse_thread_creation,
    parse_thread_pool_executor,
)


@pytest.fixture
def asyncio_fixture_path():
    """Path to asyncio fixture file."""
    return Path(__file__).parent / "fixtures" / "asyncio_patterns.py"


@pytest.fixture
def threading_fixture_path():
    """Path to threading fixture file."""
    return Path(__file__).parent / "fixtures" / "threading_patterns.py"


@pytest.fixture
def multiprocessing_fixture_path():
    """Path to multiprocessing fixture file."""
    return Path(__file__).parent / "fixtures" / "multiprocessing_patterns.py"


@pytest.fixture
def run_in_executor_fixture_path():
    """Path to run_in_executor fixture file."""
    return Path(__file__).parent / "fixtures" / "run_in_executor_patterns.py"


def test_parse_async_function(asyncio_fixture_path):
    """Test parsing async function definitions."""
    code = asyncio_fixture_path.read_text()
    module = parse(code)

    async_funcs = [node for node in module.body if node.__class__.__name__ == "AsyncFunctionDef"]
    assert len(async_funcs) >= 1

    # Parse first async function
    pattern = parse_async_function(async_funcs[0], "test.py")
    assert pattern["file"] == "test.py"
    assert pattern["function_name"] == "simple_async_function"
    assert pattern["parameters"] == []
    assert pattern["line"] > 0


def test_parse_async_function_with_params(asyncio_fixture_path):
    """Test parsing async function with parameters."""
    code = asyncio_fixture_path.read_text()
    module = parse(code)

    async_funcs = [node for node in module.body if node.__class__.__name__ == "AsyncFunctionDef"]
    # Find the function with params
    func_with_params = next((f for f in async_funcs if f.name == "async_function_with_params"), None)
    assert func_with_params is not None

    pattern = parse_async_function(func_with_params, "test.py")
    assert pattern["function_name"] == "async_function_with_params"
    assert "timeout" in pattern["parameters"]
    assert "message" in pattern["parameters"]


def test_parse_await_expression(asyncio_fixture_path):
    """Test parsing await expressions."""
    code = asyncio_fixture_path.read_text()
    module = parse(code)

    # Find all await nodes
    await_nodes = list(module.nodes_of_class(type(parse("await x").body[0].value)))
    assert len(await_nodes) > 0

    # Parse first await
    pattern = parse_await_expression(await_nodes[0], "test.py")
    assert pattern["file"] == "test.py"
    assert "awaited_expression" in pattern
    assert pattern["line"] > 0


def test_parse_async_context_manager(asyncio_fixture_path):
    """Test parsing async with statements."""
    code = asyncio_fixture_path.read_text()
    module = parse(code)

    # Find async with nodes
    async_with_nodes = list(module.nodes_of_class(type(parse("async with x: pass").body[0])))
    assert len(async_with_nodes) > 0

    pattern = parse_async_context_manager(async_with_nodes[0], "test.py")
    assert pattern["file"] == "test.py"
    assert "context_managers" in pattern
    assert len(pattern["context_managers"]) >= 1


def test_parse_asyncio_gather():
    """Test parsing asyncio.gather() calls."""
    code = """
import asyncio

async def test():
    result = await asyncio.gather(task1(), task2(), task3())
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find gather call
    gather_call = next(
        (c for c in call_nodes if hasattr(c.func, "attrname") and c.func.attrname == "gather"),
        None,
    )
    assert gather_call is not None

    pattern = parse_asyncio_gather(gather_call, "test.py")
    assert pattern["file"] == "test.py"
    assert pattern["task_count"] == 3
    assert len(pattern["tasks"]) == 3


def test_parse_asyncio_create_task():
    """Test parsing asyncio.create_task() calls."""
    code = """
import asyncio

async def test():
    task = asyncio.create_task(some_coroutine())
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find create_task call
    create_task_call = next(
        (c for c in call_nodes if hasattr(c.func, "attrname") and c.func.attrname == "create_task"),
        None,
    )
    assert create_task_call is not None

    pattern = parse_asyncio_create_task(create_task_call, "test.py")
    assert pattern["file"] == "test.py"
    assert "coroutine" in pattern


def test_parse_thread_creation():
    """Test parsing Thread creation."""
    code = """
import threading

def test():
    t = threading.Thread(target=worker, args=(1, 2))
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find Thread call
    thread_call = next(
        (c for c in call_nodes if hasattr(c.func, "attrname") and c.func.attrname == "Thread"),
        None,
    )
    assert thread_call is not None

    pattern = parse_thread_creation(thread_call, "test.py")
    assert pattern["file"] == "test.py"
    assert pattern["target"] is not None
    assert len(pattern["args"]) == 2


def test_parse_thread_pool_executor():
    """Test parsing ThreadPoolExecutor creation."""
    code = """
from concurrent.futures import ThreadPoolExecutor

def test():
    executor = ThreadPoolExecutor(max_workers=4)
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find ThreadPoolExecutor call
    executor_call = next(
        (c for c in call_nodes if hasattr(c.func, "name") and c.func.name == "ThreadPoolExecutor"),
        None,
    )
    assert executor_call is not None

    pattern = parse_thread_pool_executor(executor_call, "test.py")
    assert pattern["file"] == "test.py"
    assert pattern["max_workers"] == 4


def test_parse_process_creation():
    """Test parsing Process creation."""
    code = """
import multiprocessing

def test():
    p = multiprocessing.Process(target=compute, args=(100,))
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find Process call
    process_call = next(
        (c for c in call_nodes if hasattr(c.func, "attrname") and c.func.attrname == "Process"),
        None,
    )
    assert process_call is not None

    pattern = parse_process_creation(process_call, "test.py")
    assert pattern["file"] == "test.py"
    assert pattern["target"] is not None
    assert len(pattern["args"]) == 1


def test_parse_process_pool_executor():
    """Test parsing ProcessPoolExecutor creation."""
    code = """
from concurrent.futures import ProcessPoolExecutor

def test():
    executor = ProcessPoolExecutor(max_workers=2)
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find ProcessPoolExecutor call
    executor_call = next(
        (c for c in call_nodes if hasattr(c.func, "name") and c.func.name == "ProcessPoolExecutor"),
        None,
    )
    assert executor_call is not None

    pattern = parse_process_pool_executor(executor_call, "test.py")
    assert pattern["file"] == "test.py"
    assert pattern["max_workers"] == 2


def test_parse_run_in_executor_default():
    """Test parsing run_in_executor with default executor."""
    code = """
import asyncio

async def test():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_func)
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find run_in_executor call
    executor_call = next(
        (c for c in call_nodes if hasattr(c.func, "attrname") and c.func.attrname == "run_in_executor"),
        None,
    )
    assert executor_call is not None

    pattern = parse_run_in_executor(executor_call, "test.py", {})
    assert pattern["file"] == "test.py"
    assert pattern["executor"] == "default_thread_executor"
    assert pattern["function"] is not None
    assert pattern["_category"] == "threading"


def test_parse_run_in_executor_with_process_pool():
    """Test parsing run_in_executor with ProcessPoolExecutor."""
    code = """
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def test():
    loop = asyncio.get_event_loop()
    process_pool = ProcessPoolExecutor(max_workers=2)
    result = await loop.run_in_executor(process_pool, cpu_func, 1000)
"""
    module = parse(code)
    call_nodes = list(module.nodes_of_class(type(parse("f()").body[0].value)))

    # Find run_in_executor call
    executor_call = next(
        (c for c in call_nodes if hasattr(c.func, "attrname") and c.func.attrname == "run_in_executor"),
        None,
    )
    assert executor_call is not None

    # Provide executor type mapping
    executor_types = {"process_pool": "ProcessPoolExecutor"}
    pattern = parse_run_in_executor(executor_call, "test.py", executor_types)
    assert pattern["file"] == "test.py"
    assert pattern["executor"] == "process_pool"
    assert pattern["_category"] == "multiprocessing"
