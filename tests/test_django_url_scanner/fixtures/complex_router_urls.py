"""Complex DRF Router example with nested routers."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter


class UserViewSet:
    """User ViewSet with full CRUD operations."""

    def list(self, request):
        """List all users."""
        pass

    def create(self, request):
        """Create a new user."""
        pass

    def retrieve(self, request, pk=None):
        """Get a single user."""
        pass

    def update(self, request, pk=None):
        """Update a user."""
        pass

    def destroy(self, request, pk=None):
        """Delete a user."""
        pass


class PostViewSet:
    """Post ViewSet."""

    pass


class CommentViewSet:
    """Comment ViewSet."""

    pass


# API v1 router
api_v1_router = DefaultRouter()
api_v1_router.register(r"users", UserViewSet, basename="v1-user")
api_v1_router.register(r"posts", PostViewSet, basename="v1-post")

# API v2 router with simple router
api_v2_router = SimpleRouter()
api_v2_router.register(r"users", UserViewSet)
api_v2_router.register(r"comments", CommentViewSet)

# Main URL patterns
urlpatterns = [
    path("api/v1/", include(api_v1_router.urls)),
    path("api/v2/", include(api_v2_router.urls)),
]
