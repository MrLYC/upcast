"""Non-Django settings that should NOT be detected."""

# Local settings dictionary
settings = {
    "DATABASE_URL": "postgres://localhost/db",
    "DEBUG": True,
}

# Access local settings (should NOT be detected)
db_url = settings["DATABASE_URL"]
debug = settings.get("DEBUG")

# From project settings module (not django.conf)
# from myapp.settings import SECRET_KEY  # This would also not be detected
