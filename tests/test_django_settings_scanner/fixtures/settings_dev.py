"""Development settings that inherit from base."""

from .settings_base import *  # noqa: F403

# Override DEBUG for development
DEBUG = False

# Add development apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "debug_toolbar",
]

# Development-specific setting
DEV_MODE = True
