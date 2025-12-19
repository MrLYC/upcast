"""Fixture file for testing typed default value preservation."""

import os

# Boolean defaults
DEBUG = os.getenv("DEBUG", False)
ENABLE_CACHE = os.getenv("ENABLE_CACHE", True)

# Integer defaults
PORT = os.getenv("PORT", 8000)
MAX_CONNECTIONS = os.getenv("MAX_CONNECTIONS", 100)
TIMEOUT = os.getenv("TIMEOUT", 0)  # Falsy value

# Float defaults
RATE_LIMIT = os.getenv("RATE_LIMIT", 10.5)
THRESHOLD = os.getenv("THRESHOLD", 0.0)  # Falsy value

# None default
OPTIONAL_KEY = os.getenv("OPTIONAL_KEY", None)

# String defaults (should still work)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
EMPTY_STRING = os.getenv("EMPTY_STRING", "")  # Falsy value


# Mixed types for same variable (to test aggregation)
def get_config():
    """Function using env vars with different defaults."""
    # First usage with boolean
    debug1 = os.getenv("MULTI_TYPE", False)
    # Second usage with int
    debug2 = os.getenv("MULTI_TYPE", 0)
    return debug1, debug2
