"""Fixture: Subprocess blocking operations."""

import subprocess
import multiprocessing
from multiprocessing import Process, Pool
from concurrent.futures import ProcessPoolExecutor


def function_with_subprocess_call():
    """Function with subprocess.call."""
    subprocess.call(["echo", "hello"])


def function_with_subprocess_run():
    """Function with subprocess.run."""
    subprocess.run(["ls", "-la"], capture_output=True)


def function_with_popen():
    """Function with subprocess.Popen."""
    proc = subprocess.Popen(["python", "--version"], stdout=subprocess.PIPE)
    proc.wait()


def function_with_popen_communicate():
    """Function with Popen.communicate."""
    proc = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=b"data")


def function_with_process():
    """Function with multiprocessing.Process."""

    def worker():
        pass

    p = Process(target=worker)
    p.start()
    p.join()


def function_with_pool():
    """Function with multiprocessing.Pool."""
    with Pool(processes=4) as pool:
        result = pool.map(lambda x: x * 2, [1, 2, 3, 4])


def function_with_pool_apply():
    """Function with Pool.apply (blocking)."""
    pool = Pool(processes=2)
    result = pool.apply(lambda x: x * 2, (10,))
    pool.close()
    pool.join()


def function_with_process_pool_executor():
    """Function with ProcessPoolExecutor."""
    with ProcessPoolExecutor(max_workers=4) as executor:
        future = executor.submit(pow, 2, 3)
        result = future.result()


class ClassWithSubprocess:
    """Class with subprocess operations."""

    def method_with_call(self):
        """Method with subprocess.call."""
        return subprocess.call(["pwd"])

    def method_with_process(self):
        """Method with Process."""
        p = multiprocessing.Process(target=lambda: None)
        p.start()
        p.join(timeout=5.0)


def subprocess_in_if_block():
    """Subprocess inside if block."""
    if True:
        subprocess.run(["echo", "test"])


def subprocess_in_try_block():
    """Subprocess inside try block."""
    try:
        subprocess.call(["python", "--version"])
    except Exception:
        pass
