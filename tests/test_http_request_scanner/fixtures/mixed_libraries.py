# ruff: noqa
"""Mixed library usage patterns for testing."""

import requests
import httpx

# Same URL, different libraries
r1 = requests.get("https://example.com")
r2 = httpx.get("https://example.com")

# Different URLs
r3 = requests.post("https://api.example.com/login", json={"user": "admin"})
r4 = httpx.post("https://api.example.com/data", json={"data": "value"})
