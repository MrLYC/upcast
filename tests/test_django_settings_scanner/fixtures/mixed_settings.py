"""Mixed Django and non-Django settings."""

from django.conf import settings as django_settings

# Local settings
local_settings = {"KEY": "value"}

# Django settings (should be detected)
database = django_settings.DATABASE_URL
debug = django_settings.DEBUG

# Local settings (should NOT be detected)
local_key = local_settings["KEY"]
