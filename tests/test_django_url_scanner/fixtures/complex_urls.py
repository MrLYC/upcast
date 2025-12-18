"""Complex URL patterns with various features."""

from functools import partial

from django.urls import include, path, re_path

from .views import common_view

FEATURE_ENABLED = True


def post_list(request):
    """List all posts."""
    return None


def post_detail(request, post_id):
    """Display a single post."""
    return None


def enabled_view(request):
    """Feature-enabled view."""
    return None


def disabled_view(request):
    """Feature-disabled view."""
    return None


class EditView:
    """Generic edit view."""

    @staticmethod
    def as_view():
        """Return view function."""
        return None


urlpatterns = [
    # Basic path
    path("posts/", post_list, name="post-list"),
    # Path with converter
    path("posts/<int:id>/", post_detail, name="post-detail"),
    # Regex pattern
    re_path(r"^archive/(?P<year>\d{4})/$", post_list, name="archive"),
    # Class-based view
    path("edit/<int:id>/", EditView.as_view(), name="edit"),
    # Include
    path("api/", include("app.api.urls")),
    # functools.partial
    path("health/", partial(common_view, deep=True), name="health"),
    # Conditional view
    path("feature/", enabled_view if FEATURE_ENABLED else disabled_view, name="feature"),
]
