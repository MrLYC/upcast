"""Complex test file with mixed patterns and type inference."""

import os
from os import environ

# Type conversions
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
ENABLE_CACHE = bool(os.getenv("ENABLE_CACHE", "True"))
RATE_LIMIT = float(os.getenv("RATE_LIMIT", "10.5"))

# Or expressions for defaults
LOG_LEVEL = os.getenv("LOG_LEVEL") or "INFO"
USE_SSL = environ.get("USE_SSL") or True
WORKERS = int(environ.get("WORKERS", "4")) or 1

# String concatenation
PREFIX = "APP_"
CONFIG_KEY = os.getenv(PREFIX + "CONFIG")

# Multiple usages of same variable
DB_HOST = os.getenv("DB_HOST", "localhost")
db_connection = f"postgresql://{os.getenv('DB_HOST')}:5432/db"
