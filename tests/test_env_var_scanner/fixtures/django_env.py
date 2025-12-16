"""Test file with django-environ patterns."""

import environ

env = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(list, []))

# Read .env file
# environ.Env.read_env()

# Django-environ typed methods
DATABASE_URL = env.str("DATABASE_URL")
DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")
PORT = env.int("PORT", 8000)
TIMEOUT = env.float("TIMEOUT", 30.0)

# Without type
CUSTOM_VAR = env("CUSTOM_VAR", default="value")
REQUIRED_VAR = env("REQUIRED_VAR")
