"""Integration test for concurrency scanner with enhanced pattern detection."""

from pathlib import Path
from textwrap import dedent

import pytest

from upcast.scanners.concurrency import ConcurrencyScanner


@pytest.fixture
def temp_test_file(tmp_path: Path) -> Path:
    """Create a temporary test file with concurrency patterns."""
    test_file = tmp_path / "test_concurrency_patterns.py"
    test_file.write_text(
        dedent(
            """
            import threading
            import multiprocessing
            import asyncio
            from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

            # Thread creation
            def create_thread():
                t = threading.Thread(target=worker_function, name="worker")
                t.start()

            def worker_function():
                pass

            # ThreadPoolExecutor
            thread_pool = ThreadPoolExecutor(max_workers=4)

            def use_thread_pool():
                future = thread_pool.submit(worker_function)
                return future

            # Process creation
            def create_process():
                p = multiprocessing.Process(target=worker_function, name="worker_process")
                p.start()

            # ProcessPoolExecutor
            process_pool = ProcessPoolExecutor(max_workers=2)

            def use_process_pool():
                future = process_pool.submit(worker_function)
                return future

            # Asyncio patterns
            async def async_worker():
                await asyncio.sleep(1)

            async def create_task_example():
                task = asyncio.create_task(async_worker())
                await task

            # run_in_executor
            async def run_in_executor_example():
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(thread_pool, worker_function)
                result2 = await loop.run_in_executor(process_pool, worker_function)
                return result, result2

            # Class-based example
            class ConcurrencyManager:
                def __init__(self):
                    self.executor = ThreadPoolExecutor(max_workers=8)

                def submit_work(self):
                    return self.executor.submit(self.worker)

                def worker(self):
                    pass
            """
        )
    )
    return test_file


def test_thread_creation_detection(temp_test_file: Path):
    """Test Thread creation pattern detection with details."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    # Find thread creation patterns
    thread_patterns = output.results.get("threading", {})
    thread_creation = thread_patterns.get("thread_creation", [])

    assert len(thread_creation) > 0, "Should detect Thread creation"

    pattern = thread_creation[0]
    assert pattern.pattern == "thread_creation"
    assert pattern.function == "create_thread"
    assert pattern.details is not None
    assert "target" in pattern.details


def test_threadpool_executor_detection(temp_test_file: Path):
    """Test ThreadPoolExecutor creation with max_workers."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    thread_patterns = output.results.get("threading", {})
    thread_pool = thread_patterns.get("thread_pool_executor", [])

    assert len(thread_pool) >= 2, "Should detect ThreadPoolExecutor creations"

    # Check module-level executor
    module_level = [p for p in thread_pool if p.function is None]
    assert len(module_level) > 0

    pattern = module_level[0]
    assert pattern.details is not None
    assert pattern.details.get("max_workers") == 4 or pattern.details.get("max_workers") == 8


def test_executor_submit_resolution(temp_test_file: Path):
    """Test executor.submit() resolution with executor mapping."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    thread_patterns = output.results.get("threading", {})
    submit_patterns = thread_patterns.get("submit", [])

    assert len(submit_patterns) >= 1, "Should detect executor.submit() calls"

    # Check that function is in details
    pattern = submit_patterns[0]
    assert pattern.api_call == "submit"
    assert pattern.details is not None
    assert "function" in pattern.details


def test_process_creation_detection(temp_test_file: Path):
    """Test Process creation pattern detection."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    process_patterns = output.results.get("multiprocessing", {})
    process_creation = process_patterns.get("process_creation", [])

    assert len(process_creation) > 0, "Should detect Process creation"

    pattern = process_creation[0]
    assert pattern.pattern == "process_creation"
    assert pattern.function == "create_process"
    assert pattern.details is not None
    assert "target" in pattern.details


def test_processpool_executor_detection(temp_test_file: Path):
    """Test ProcessPoolExecutor creation with max_workers."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    process_patterns = output.results.get("multiprocessing", {})
    process_pool = process_patterns.get("process_pool_executor", [])

    assert len(process_pool) > 0, "Should detect ProcessPoolExecutor creation"

    pattern = process_pool[0]
    assert pattern.details is not None
    assert pattern.details.get("max_workers") == 2


def test_create_task_detection(temp_test_file: Path):
    """Test asyncio.create_task() detection with coroutine resolution."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    asyncio_patterns = output.results.get("asyncio", {})
    create_task_patterns = asyncio_patterns.get("create_task", [])

    assert len(create_task_patterns) > 0, "Should detect asyncio.create_task()"

    pattern = create_task_patterns[0]
    assert pattern.api_call == "create_task"
    assert pattern.function == "create_task_example"
    assert pattern.details is not None
    assert "coroutine" in pattern.details


def test_run_in_executor_resolution(temp_test_file: Path):
    """Test run_in_executor() detection with executor type resolution."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    # Should have both thread and process executor usages
    thread_patterns = output.results.get("threading", {})
    run_in_exec_thread = thread_patterns.get("run_in_executor", [])

    process_patterns = output.results.get("multiprocessing", {})
    run_in_exec_process = process_patterns.get("run_in_executor", [])

    assert len(run_in_exec_thread) > 0, "Should detect thread executor usage"
    assert len(run_in_exec_process) > 0, "Should detect process executor usage"

    # Check thread executor
    thread_pattern = run_in_exec_thread[0]
    assert thread_pattern.api_call == "run_in_executor"
    assert thread_pattern.details is not None
    assert thread_pattern.details["executor_type"] == "ThreadPoolExecutor"

    # Check process executor
    process_pattern = run_in_exec_process[0]
    assert process_pattern.details["executor_type"] == "ProcessPoolExecutor"


def test_class_context_extraction(temp_test_file: Path):
    """Test extraction of class context for methods."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    thread_patterns = output.results.get("threading", {})

    # Find patterns inside ConcurrencyManager class
    class_patterns = []
    for pattern_type, usages in thread_patterns.items():
        for usage in usages:
            if usage.class_name == "ConcurrencyManager":
                class_patterns.append(usage)

    assert len(class_patterns) >= 1, "Should detect patterns in class methods"

    # Check that function and class_name are set
    for pattern in class_patterns:
        assert pattern.class_name == "ConcurrencyManager"
        assert pattern.function in ("__init__", "submit_work")


def test_async_function_detection(temp_test_file: Path):
    """Test async function declarations are detected."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    asyncio_patterns = output.results.get("asyncio", {})
    async_functions = asyncio_patterns.get("async_function", [])

    assert len(async_functions) >= 3, "Should detect all async function definitions"

    func_names = {p.statement for p in async_functions}
    assert any("async_worker" in s for s in func_names)
    assert any("create_task_example" in s for s in func_names)
    assert any("run_in_executor_example" in s for s in func_names)


def test_summary_statistics(temp_test_file: Path):
    """Test summary statistics are calculated correctly."""
    scanner = ConcurrencyScanner()
    output = scanner.scan(temp_test_file.parent)

    summary = output.summary

    # Should have patterns in multiple categories
    assert summary.total_count > 0
    assert summary.files_scanned == 1
    assert summary.scan_duration_ms > 0

    assert "threading" in summary.by_category
    assert "multiprocessing" in summary.by_category
    assert "asyncio" in summary.by_category

    # Verify counts match
    total_from_categories = sum(summary.by_category.values())
    assert total_from_categories == summary.total_count
