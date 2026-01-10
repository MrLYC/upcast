"""Fixture: Mixed contexts for blocking operations."""

import time
import threading
import subprocess


# Module level
time.sleep(0.1)
lock = threading.Lock()


def simple_function():
    """Simple function with blocking operations."""
    time.sleep(1)
    subprocess.call(["echo", "hello"])


class SimpleClass:
    """Simple class with blocking operations."""

    def __init__(self):
        self.lock = threading.Lock()
        time.sleep(0.5)

    def method(self):
        """Method with blocking operation."""
        with self.lock:
            time.sleep(0.1)


def function_with_if():
    """Function with if block."""
    if True:
        time.sleep(1)
    else:
        subprocess.run(["ls"])


def function_with_for():
    """Function with for loop."""
    for i in range(3):
        time.sleep(0.1)


def function_with_while():
    """Function with while loop."""
    i = 0
    while i < 3:
        time.sleep(0.1)
        i += 1


def function_with_try():
    """Function with try block."""
    try:
        time.sleep(1)
        subprocess.call(["test"])
    except Exception:
        pass


def function_with_nested_blocks():
    """Function with nested blocks."""
    if True:
        for i in range(2):
            try:
                time.sleep(0.1)
            except:
                pass


class ClassWithNestedBlocks:
    """Class with nested block structures."""

    def method_with_if(self):
        """Method with if block."""
        if True:
            lock = threading.Lock()
            with lock:
                pass

    def method_with_loop(self):
        """Method with loop."""
        for i in range(5):
            time.sleep(0.05)


def function_with_with_statement():
    """Function with 'with' statement."""
    with threading.Lock():
        time.sleep(0.1)


async def async_function_mixed():
    """Async function with mixed operations."""
    import asyncio

    await asyncio.sleep(1)
    # Note: This would be bad practice - mixing async/sync
    time.sleep(0.1)


def deeply_nested():
    """Deeply nested blocks."""
    if True:
        while True:
            try:
                for i in range(1):
                    with threading.Lock():
                        if i == 0:
                            time.sleep(0.1)
                break
            except:
                pass
