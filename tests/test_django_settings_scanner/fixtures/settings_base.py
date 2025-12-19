"""Base settings module for testing inheritance."""

DEBUG = True
SECRET_KEY = "base-secret-key"  # noqa: S105

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

DATABASE_NAME = "base_db"
