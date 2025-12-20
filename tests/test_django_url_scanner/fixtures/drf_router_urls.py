"""DRF Router URL patterns."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter


class UserViewSet:
    """User ViewSet."""

    def list(self, request):
        """List all users."""
        pass

    def retrieve(self, request, pk=None):
        """Retrieve a single user."""
        pass


class PostViewSet:
    """Post ViewSet."""

    def list(self, request):
        """List all posts."""
        pass

    def create(self, request):
        """Create a new post."""
        pass


# DefaultRouter with explicit basename
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"posts", PostViewSet)

# SimpleRouter
simple_router = SimpleRouter()
simple_router.register(r"products", UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("simple/", include(simple_router.urls)),
]
