"""URL patterns with dynamic construction."""

from django.urls import path


def view_a(request):
    """View A."""
    return None


def view_b(request):
    """View B."""
    return None


# Dynamic urlpatterns using list comprehension
urlpatterns = [path(f"item{i}/", view_a, name=f"item-{i}") for i in range(3)]

# Extended urlpatterns
urlpatterns += [
    path("extra/", view_b, name="extra"),
]
