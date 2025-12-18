"""Test fixtures with mixed concurrency patterns."""

import asyncio
import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def blocking_task(item_id: int):
    """A blocking task."""
    return item_id * 2


def cpu_intensive_task(number: int):
    """A CPU-intensive task."""
    return number**2


class MixedConcurrencyApp:
    """Application using multiple concurrency approaches."""

    def __init__(self):
        """Initialize with executors."""
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.process_pool = ProcessPoolExecutor(max_workers=2)

    async def async_with_threads(self, items: list[int]):
        """Async function that uses threads via run_in_executor."""
        loop = asyncio.get_event_loop()
        results = []
        for item_id in items:
            result = await loop.run_in_executor(self.thread_pool, blocking_task, item_id)
            results.append(result)
        return results

    async def async_with_processes(self, numbers: list[int]):
        """Async function that uses processes via run_in_executor."""
        loop = asyncio.get_event_loop()
        results = []
        for number in numbers:
            result = await loop.run_in_executor(self.process_pool, cpu_intensive_task, number)
            results.append(result)
        return results

    async def pure_asyncio(self):
        """Pure asyncio without executors."""
        task1 = asyncio.create_task(self.async_helper())
        task2 = asyncio.create_task(self.async_helper())
        return await asyncio.gather(task1, task2)

    async def async_helper(self):
        """Helper async function."""
        await asyncio.sleep(0.1)
        return "done"

    def thread_worker(self):
        """Worker function for threads."""
        thread = threading.Thread(target=blocking_task, args=(1,))
        thread.start()
        thread.join()

    def process_worker(self):
        """Worker function for processes."""
        process = multiprocessing.Process(target=cpu_intensive_task, args=(100,))
        process.start()
        process.join()


async def complex_async_workflow():
    """Complex async workflow with mixed patterns."""
    app = MixedConcurrencyApp()

    # Use asyncio.gather to run multiple async operations
    thread_results, process_results, pure_results = await asyncio.gather(
        app.async_with_threads([1, 2, 3]),
        app.async_with_processes([10, 20, 30]),
        app.pure_asyncio(),
    )

    return thread_results, process_results, pure_results


def run_with_default_executor():
    """Use run_in_executor with default (thread) executor."""

    async def helper():
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, blocking_task, 5)
        return result

    return asyncio.run(helper())
