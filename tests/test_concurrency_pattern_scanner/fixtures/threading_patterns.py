"""Test fixtures for threading patterns."""

import threading
from concurrent.futures import ThreadPoolExecutor


def worker_function(item_id: int):
    """Simple worker function."""
    return item_id * 2


def create_simple_thread():
    """Create a simple thread."""
    thread = threading.Thread(target=worker_function, args=(1,))
    thread.start()
    thread.join()


def create_multiple_threads():
    """Create multiple threads."""
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker_function, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def use_thread_pool_executor():
    """Use ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker_function, i) for i in range(10)]
        results = [future.result() for future in futures]
    return results


def use_thread_pool_with_variable():
    """Use ThreadPoolExecutor with variable."""
    executor = ThreadPoolExecutor(max_workers=2)
    future = executor.submit(worker_function, 5)
    result = future.result()
    executor.shutdown()
    return result


class ThreadedClass:
    """Class using threading."""

    def run_in_thread(self, item_id: int):
        """Run worker in a thread."""
        thread = threading.Thread(target=worker_function, args=(item_id,))
        thread.start()
        return thread
