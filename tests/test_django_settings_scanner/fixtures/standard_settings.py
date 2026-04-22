import os

ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
ALLOWED_HOSTS = ["localhost", os.environ.get("EXTERNAL_HOST")]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
    }
]
