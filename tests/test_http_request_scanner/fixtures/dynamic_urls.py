# ruff: noqa
"""Dynamic URL patterns for testing."""

import requests

# F-string with constant
API_BASE = "https://api.example.com"
response = requests.get(f"{API_BASE}/users")

# String concatenation
BASE_URL = "https://api.example.com"
response = requests.get(BASE_URL + "/data")

# Format string
response = requests.get("{}/items".format(API_BASE))


# Dynamic URL (unresolvable)
def fetch(endpoint):
    return requests.get(f"https://api.example.com/{endpoint}")


# Runtime variable (unresolvable)
def fetch_by_id(resource_id):
    url = f"https://api.example.com/resource/{resource_id}"
    return requests.get(url)
