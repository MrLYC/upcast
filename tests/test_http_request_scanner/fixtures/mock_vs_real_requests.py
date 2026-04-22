# ruff: noqa
"""Fixture that separates mock registration calls from real session-based HTTP usage."""

import aiohttp
import httpx
import requests_mock


# These are mock registrations and should never be treated as real outbound requests.
requests_mock.get("https://mock.example.com/users", text="ok")
requests_mock.post("https://mock.example.com/orders", json={"status": "created"})


with httpx.Client() as client:
    client.get("https://real.example.com/httpx-sync")


async def fetch_with_httpx_async_client():
    async with httpx.AsyncClient() as client:
        await client.post("https://real.example.com/httpx-async", json={"ok": True})


async def fetch_with_aiohttp_session():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://real.example.com/aiohttp-session") as response:
            return await response.text()
