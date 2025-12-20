"""Sample code with blocking operations for testing."""

import subprocess
import threading
import time
from subprocess import Popen


def blocking_sleep():
    """Function with time.sleep()."""
    time.sleep(5)
    print("Done sleeping")


def variable_sleep():
    """Function with variable sleep duration."""
    timeout = 10
    time.sleep(timeout)


async def async_with_sleep():
    """Async function with blocking sleep (anti-pattern)."""
    time.sleep(1)
    return "bad"


def subprocess_operations():
    """Function with subprocess operations."""
    # subprocess.run with timeout
    subprocess.run(["ls", "-la"], timeout=30)  # noqa: S603, S607

    # Popen operations
    proc = Popen(["echo", "hello"])  # noqa: S603, S607
    proc.wait(timeout=5)

    proc2 = Popen(["cat"], stdin=subprocess.PIPE)  # noqa: S603, S607
    proc2.communicate(input=b"test", timeout=10)


def lock_operations():
    """Function with lock operations."""
    lock = threading.Lock()
    lock.acquire(timeout=5)
    lock.release()

    rlock = threading.RLock()
    rlock.acquire(blocking=True)
    rlock.release()

    sem = threading.Semaphore()
    sem.acquire(timeout=1)
    sem.release()


def lock_context_manager():
    """Function using lock with context manager."""
    with threading.Lock():
        print("Critical section")

    with threading.RLock():
        print("Reentrant section")


class MyClass:
    """Class with blocking operations."""

    def method_with_sleep(self):
        """Method with sleep."""
        time.sleep(2)

    async def async_method_with_lock(self):
        """Async method with lock (anti-pattern)."""
        lock = threading.Lock()
        lock.acquire()
        try:
            print("locked")
        finally:
            lock.release()
