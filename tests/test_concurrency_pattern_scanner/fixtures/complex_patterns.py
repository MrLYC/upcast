"""Test fixtures with complex and edge case concurrency patterns."""

import asyncio
from concurrent.futures import ThreadPoolExecutor


def nested_function_worker():
    """Nested function with thread creation."""
    import threading

    def inner_worker(item_id: int):
        return item_id

    thread = threading.Thread(target=inner_worker, args=(1,))
    thread.start()
    return thread


class ComplexAsyncClass:
    """Class with complex async patterns."""

    async def method_with_nested_gather(self):
        """Method with nested gather calls."""
        inner_results = await asyncio.gather(
            self.helper_async(1),
            self.helper_async(2),
        )

        outer_results = await asyncio.gather(
            asyncio.create_task(self.process_results(inner_results)),
            asyncio.create_task(self.helper_async(3)),
        )

        return outer_results

    async def helper_async(self, item_id: int):
        """Helper async method."""
        await asyncio.sleep(0.01)
        return item_id

    async def process_results(self, results: list):
        """Process results asynchronously."""
        await asyncio.sleep(0.01)
        return sum(results)


class ConditionalConcurrency:
    """Class with conditional concurrency patterns."""

    def __init__(self, use_threads: bool):
        """Initialize with configuration."""
        self.use_threads = use_threads
        if use_threads:
            self.executor = ThreadPoolExecutor(max_workers=2)
        else:
            from concurrent.futures import ProcessPoolExecutor

            self.executor = ProcessPoolExecutor(max_workers=2)

    async def run_with_executor(self, func, *args):
        """Run function with configured executor."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args)


def dynamic_thread_creation(count: int):
    """Dynamically create threads based on count."""
    import threading

    threads = []
    for i in range(count):
        thread = threading.Thread(target=lambda x: x * 2, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


async def async_context_managers():
    """Multiple async context managers."""
    async with asyncio.Lock():
        await asyncio.sleep(0.01)

    async with asyncio.Semaphore(5):
        await asyncio.sleep(0.01)

    # Nested context managers
    async with asyncio.Lock(), asyncio.Condition():
        await asyncio.sleep(0.01)


class NestedClass:
    """Class with nested class containing async methods."""

    class InnerAsync:
        """Inner class with async methods."""

        async def inner_async_method(self):
            """Async method in nested class."""
            await asyncio.sleep(0.01)
            return "nested"

        async def inner_with_gather(self):
            """Inner method with gather."""
            return await asyncio.gather(
                self.inner_async_method(),
                self.inner_async_method(),
            )


def lambda_with_threads():
    """Using lambda functions with threads."""
    import threading

    operations = [lambda x: x * 2, lambda x: x + 10, lambda x: x**2]

    threads = [threading.Thread(target=op, args=(i,)) for i, op in enumerate(operations)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


async def comprehension_with_tasks():
    """Using list comprehension with asyncio tasks."""
    tasks = [asyncio.create_task(asyncio.sleep(0.01)) for _ in range(5)]
    await asyncio.gather(*tasks)


def executor_in_function():
    """Executor created and used within function."""
    from concurrent.futures import ThreadPoolExecutor

    def worker(item_id: int):
        return item_id * 2

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        results = [f.result() for f in futures]

    return results
