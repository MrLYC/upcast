"""Example showing all URL pattern types."""

from django.urls import include, path, re_path


def index_view(request):
    """Home page."""
    return None


def detail_view(request, item_id):
    """Detail view."""
    return None


urlpatterns = [
    # Type: path
    path("", index_view, name="index"),
    # Type: path with converter
    path("detail/<int:id>/", detail_view, name="detail"),
    # Type: re_path
    re_path(r"^archive/(?P<year>\d{4})/$", index_view, name="archive"),
    # Type: include
    path("api/", include("myapp.api.urls"), name="api"),
]
