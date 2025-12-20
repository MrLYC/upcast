"""Decorator pattern examples for testing."""

from prometheus_client import Counter, Histogram

# Define metrics
function_calls_total = Counter("function_calls_total", "函数调用次数")
request_time_seconds = Histogram("request_time_seconds", "Request processing time")


@function_calls_total.count_exceptions()
def risky_function():
    """Function that might raise exceptions."""
    pass


@request_time_seconds.time()
def process_request():
    """Function that we want to time."""
    pass


# Multiple decorators
@function_calls_total.count_exceptions(Exception)
@request_time_seconds.time()
def complex_function():
    """Function with multiple metric decorators."""
    pass
