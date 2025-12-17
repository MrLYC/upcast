"""Aliased imports."""

from django.conf import settings as config

# Using aliased settings
database = config.DATABASE_URL
debug = config.DEBUG

# getattr with alias
api_key = getattr(config, "API_KEY", "default")
