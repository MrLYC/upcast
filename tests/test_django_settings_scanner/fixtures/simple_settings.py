"""Simple Django settings usage patterns."""

from django.conf import settings

# Basic attribute access
database_url = settings.DATABASE_URL
debug_mode = settings.DEBUG

# Nested attribute access
default_db = settings.DATABASES["default"]

# In conditionals
if settings.DEBUG:
    print("Debug mode enabled")

# In expressions
base_url = f"{settings.BASE_URL}/api"
