"""Settings module with dynamic imports for testing."""

import importlib
import os

# Dynamic import using f-string
env = os.environ.get("ENV", "dev")
settings_module = importlib.import_module(f"settings.{env}")

# Dynamic import using string concatenation
profile = "production"
config = importlib.import_module("config." + profile)

# Dynamic import using format()
app_name = "myapp"
app_settings = importlib.import_module(f"apps.{app_name}.settings")

# Static import (should not be detected)
base_settings = importlib.import_module("settings.base")
