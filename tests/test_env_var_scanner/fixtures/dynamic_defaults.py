"""Fixture file for testing dynamic default value filtering."""

import os

# Dynamic default - should be excluded from defaults list
BK_CC_HOST = os.getenv("BK_CC_HOST", os.getenv("OTHER", ""))

# Dynamic default with more complex expression
API_URL = os.getenv("API_URL", os.environ.get("FALLBACK_API", "http://default"))

# Simple static default - should be included
STATIC_DEFAULT = os.getenv("STATIC_DEFAULT", "http://example.com")


# Multiple usages with mixed static/dynamic defaults
def get_database_url():
    """Function with dynamic and static defaults."""
    # Static default
    db1 = os.getenv("DB_URL", "postgresql://localhost/db")
    # Dynamic default
    db2 = os.getenv("DB_URL", os.getenv("BACKUP_DB", ""))
    return db1, db2


# Edge cases
ONLY_DYNAMIC = os.getenv("ONLY_DYNAMIC", os.getenv("FALLBACK", "default"))
MIXED_ORDER_1 = os.getenv("MIXED_VAR", "static1")
MIXED_ORDER_2 = os.getenv("MIXED_VAR", os.getenv("DYNAMIC", ""))
MIXED_ORDER_3 = os.getenv("MIXED_VAR", "static2")
