"""Simple URL patterns for testing."""

from django.urls import path


def index(request):
    """Home page view."""
    return None


def detail(request, item_id):
    """Detail view for a specific item."""
    return None


urlpatterns = [
    path("", index, name="index"),
    path("detail/<int:id>/", detail, name="detail"),
]
