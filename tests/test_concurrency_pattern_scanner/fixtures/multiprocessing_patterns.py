"""Test fixtures for multiprocessing patterns."""

import multiprocessing
from concurrent.futures import ProcessPoolExecutor


def compute_function(number: int):
    """Simple compute function."""
    return number**2


def create_simple_process():
    """Create a simple process."""
    process = multiprocessing.Process(target=compute_function, args=(10,))
    process.start()
    process.join()


def create_multiple_processes():
    """Create multiple processes."""
    processes = []
    for i in range(3):
        process = multiprocessing.Process(target=compute_function, args=(i,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


def use_process_pool_executor():
    """Use ProcessPoolExecutor."""
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(compute_function, i) for i in range(5)]
        results = [future.result() for future in futures]
    return results


def use_process_pool_with_variable():
    """Use ProcessPoolExecutor with variable."""
    executor = ProcessPoolExecutor(max_workers=4)
    future = executor.submit(compute_function, 100)
    result = future.result()
    executor.shutdown()
    return result


class MultiprocessingClass:
    """Class using multiprocessing."""

    def run_in_process(self, number: int):
        """Run compute in a process."""
        process = multiprocessing.Process(target=compute_function, args=(number,))
        process.start()
        return process
