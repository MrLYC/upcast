# ruff: noqa
"""httpx library usage patterns for testing."""

import httpx
import asyncio

# Sync GET
r = httpx.get("https://example.com")

# Sync POST
r = httpx.post("https://api.example.com/data", json={"key": "value"})

# Sync client
with httpx.Client() as client:
    r = client.get("https://example.com")


# Async GET
async def fetch():
    r = await httpx.get("https://example.com/async")
    return r


# Async client
async def fetch_with_client():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://example.com")
        r = await client.post("https://api.example.com/data", json={"data": "value"})
