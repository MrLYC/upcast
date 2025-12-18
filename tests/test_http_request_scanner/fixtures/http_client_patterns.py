# ruff: noqa
"""http.client usage patterns for testing."""

import http.client

# HTTPS connection
conn = http.client.HTTPSConnection("example.com")
conn.request("GET", "/")
resp = conn.getresponse()
print(resp.status, resp.read())
conn.close()

# HTTP connection
conn = http.client.HTTPConnection("example.com")
conn.request("POST", "/api/data", body='{"key": "value"}')
resp = conn.getresponse()
conn.close()

# With headers
conn = http.client.HTTPSConnection("api.example.com")
conn.request(
    "POST",
    "/endpoint",
    headers={"Content-Type": "application/json", "Authorization": "Bearer token"},
)
resp = conn.getresponse()
conn.close()
