"""Fixture: Time-based blocking operations."""

import time
import asyncio


# Module-level sleep
time.sleep(1)


def function_with_sleep():
    """Function with time.sleep."""
    time.sleep(0.5)
    return "done"


def function_with_timeout_sleep():
    """Function with timeout parameter."""
    timeout = 2.0
    time.sleep(timeout)


async def async_function_with_sleep():
    """Async function with asyncio.sleep."""
    await asyncio.sleep(1.0)
    return "done"


async def async_with_timeout():
    """Async function with timeout parameter."""
    timeout = 3.0
    await asyncio.sleep(timeout)


class ClassWithSleep:
    """Class containing sleep operations."""

    def method_with_sleep(self):
        """Method with time.sleep."""
        time.sleep(0.1)

    async def async_method_with_sleep(self):
        """Async method with asyncio.sleep."""
        await asyncio.sleep(0.2)


def sleep_in_if_block():
    """Sleep inside if block."""
    if True:
        time.sleep(1)


def sleep_in_loop():
    """Sleep inside loop."""
    for i in range(5):
        time.sleep(0.1)

    while False:
        time.sleep(0.5)
