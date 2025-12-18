"""Test fixtures for asyncio patterns."""

import asyncio


async def simple_async_function():
    """Simple async function."""
    await asyncio.sleep(1)


async def async_function_with_params(timeout: int, message: str):
    """Async function with parameters."""
    await asyncio.sleep(timeout)
    return message


async def async_with_gather():
    """Async function using gather."""
    results = await asyncio.gather(
        simple_async_function(),
        async_function_with_params(2, "test"),
        asyncio.sleep(3),
    )
    return results


async def async_with_create_task():
    """Async function using create_task."""
    task1 = asyncio.create_task(simple_async_function())
    task2 = asyncio.create_task(async_function_with_params(2, "test"))
    await task1
    await task2


async def async_with_context_manager():
    """Async function with async context manager."""
    async with asyncio.Lock():
        await asyncio.sleep(1)


class AsyncClass:
    """Class with async methods."""

    async def async_method(self):
        """Async method."""
        await asyncio.sleep(1)

    async def async_method_with_gather(self):
        """Async method using gather."""
        return await asyncio.gather(
            self.async_method(),
            simple_async_function(),
        )
