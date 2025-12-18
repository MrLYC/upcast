# ruff: noqa
"""urllib3 and urllib.request usage patterns for testing."""

import urllib3
from urllib.request import urlopen, Request

# urllib3 PoolManager
http = urllib3.PoolManager()
r = http.request("GET", "https://example.com")
print(r.status, r.data)

# urllib3 with parameters
r = http.request(
    "POST",
    "https://api.example.com/data",
    fields={"param": "value"},
    headers={"Content-Type": "application/json"},
)

# urllib.request urlopen
with urlopen("https://example.com") as resp:
    data = resp.read()

# urllib.request with Request object
req = Request(
    "https://example.com",
    headers={"User-Agent": "MyApp/1.0"},
)
with urlopen(req) as resp:
    data = resp.read()
