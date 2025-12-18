"""Test fixtures for run_in_executor patterns."""

import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def blocking_io_function():
    """Blocking I/O function."""
    with open("/dev/null", "w") as f:
        f.write("test")


def cpu_intensive_function(number: int):
    """CPU intensive function."""
    return sum(i * i for i in range(number))


async def run_in_default_executor():
    """Run in default (thread) executor."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_io_function)
    return result


async def run_in_thread_executor():
    """Run in explicit thread executor."""
    loop = asyncio.get_event_loop()
    thread_executor = ThreadPoolExecutor(max_workers=2)
    result = await loop.run_in_executor(thread_executor, blocking_io_function)
    thread_executor.shutdown()
    return result


async def run_in_process_executor():
    """Run in process executor."""
    loop = asyncio.get_event_loop()
    process_executor = ProcessPoolExecutor(max_workers=4)
    result = await loop.run_in_executor(process_executor, cpu_intensive_function, 10000)
    process_executor.shutdown()
    return result


class ExecutorBridgeClass:
    """Class using executor bridge."""

    async def run_with_thread_executor(self):
        """Run blocking function with thread executor."""
        loop = asyncio.get_event_loop()
        thread_pool = ThreadPoolExecutor(max_workers=1)
        result = await loop.run_in_executor(thread_pool, blocking_io_function)
        thread_pool.shutdown()
        return result

    async def run_with_process_executor(self):
        """Run CPU-intensive function with process executor."""
        loop = asyncio.get_event_loop()
        process_pool = ProcessPoolExecutor(max_workers=2)
        result = await loop.run_in_executor(process_pool, cpu_intensive_function, 50000)
        process_pool.shutdown()
        return result
