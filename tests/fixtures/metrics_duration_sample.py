from prometheus_client import Counter


requests_total = Counter("http_requests_total", "Total requests")
