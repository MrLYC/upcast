"""Simple test file with basic environment variable patterns."""

import os
from os import getenv

# Basic os.getenv patterns
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG", "False")
PORT = int(os.getenv("PORT", "8000"))

# os.environ patterns
API_KEY = os.environ["API_KEY"]
SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret")

# Aliased imports
MAX_CONNECTIONS = getenv("MAX_CONNECTIONS", "10")
