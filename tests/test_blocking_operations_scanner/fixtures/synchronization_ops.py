"""Fixture: Synchronization blocking operations."""

import threading
import asyncio
from threading import Lock, RLock, Semaphore, BoundedSemaphore, Event, Condition
from multiprocessing import Lock as MPLock


# Module-level lock creation
module_lock = threading.Lock()


def function_with_lock():
    """Function with threading.Lock."""
    lock = threading.Lock()
    with lock:
        pass


def function_with_rlock():
    """Function with RLock."""
    lock = threading.RLock()
    lock.acquire()
    lock.release()


def function_with_semaphore():
    """Function with Semaphore."""
    sem = threading.Semaphore(5)
    sem.acquire()
    sem.release()


def function_with_bounded_semaphore():
    """Function with BoundedSemaphore."""
    sem = threading.BoundedSemaphore(3)
    with sem:
        pass


def function_with_event():
    """Function with Event."""
    event = threading.Event()
    event.wait(timeout=2.0)


def function_with_condition():
    """Function with Condition."""
    cond = threading.Condition()
    with cond:
        cond.wait()


async def async_function_with_lock():
    """Async function with asyncio.Lock."""
    lock = asyncio.Lock()
    async with lock:
        pass


async def async_function_with_semaphore():
    """Async function with asyncio.Semaphore."""
    sem = asyncio.Semaphore(10)
    async with sem:
        await asyncio.sleep(0.1)


async def async_function_with_event():
    """Async function with asyncio.Event."""
    event = asyncio.Event()
    await event.wait()


class ClassWithLocks:
    """Class with various synchronization primitives."""

    def __init__(self):
        self.lock = threading.Lock()
        self.rlock = threading.RLock()

    def method_with_lock(self):
        """Method using lock."""
        with self.lock:
            pass

    def method_with_explicit_acquire(self):
        """Method with explicit lock acquire."""
        self.lock.acquire()
        try:
            pass
        finally:
            self.lock.release()


def multiprocessing_lock():
    """Function with multiprocessing.Lock."""
    from multiprocessing import Lock

    lock = Lock()
    with lock:
        pass
