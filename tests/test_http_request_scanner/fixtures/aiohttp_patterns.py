# ruff: noqa
"""aiohttp library usage patterns for testing."""

import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com") as resp:
            text = await resp.text()

        async with session.post(
            "https://api.example.com/data",
            json={"key": "value"},
            headers={"Auth": "token"},
        ) as resp:
            data = await resp.json()


async def with_timeout():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com", timeout=10) as resp:
            return await resp.text()
