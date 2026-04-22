# ruff: noqa
"""Fixture that proves session/client resolution must not leak across scopes."""

import httpx


def real_http_client():
    client = httpx.Client()
    client.get("https://real.example.com/in-scope")


def unrelated_client_name():
    class FakeClient:
        def get(self, url):
            return url

    client = FakeClient()
    client.get("https://fake.example.com/not-http")
