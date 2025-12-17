"""getattr and hasattr patterns."""

from django.conf import settings


def enable_new_feature() -> None:
    """Placeholder function for testing."""
    pass


# getattr without default
api_key = settings.API_KEY

# getattr with default
timeout = getattr(settings, "TIMEOUT", 30)
feature_flag = getattr(settings, "FEATURE_ENABLED", False)

# hasattr for feature flags
if hasattr(settings, "NEW_FEATURE"):
    enable_new_feature()

# hasattr in expression
has_custom = hasattr(settings, "CUSTOM_BACKEND")
