from django.urls import include, path
from . import views


urlpatterns = [
    path(
        "api/",
        include([
            path(
                "v1/",
                include([
                    path("users/", views.user_list, name="user-list"),
                ]),
            ),
        ]),
    ),
]
