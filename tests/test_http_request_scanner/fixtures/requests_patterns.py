# ruff: noqa
"""requests library usage patterns for testing."""

import requests

# Simple GET
response = requests.get("https://api.example.com/users")

# GET with parameters
response = requests.get(
    "https://api.example.com/users",
    params={"page": 1, "limit": 10},
    headers={"Authorization": "Bearer token"},
    timeout=5,
)

# POST with JSON
response = requests.post(
    "https://api.example.com/login",
    json={"username": "admin", "password": "secret"},
)

# Session usage
session = requests.Session()
response = session.get("https://api.example.com/users")
response = session.post(
    "https://api.example.com/login",
    json={"username": "admin"},
)
session.close()

# Session with context manager
with requests.Session() as s:
    s.headers.update({"Authorization": "Bearer token"})
    s.get("https://api.example.com/a")
    s.get("https://api.example.com/b")
