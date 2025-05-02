from django.urls import URLPattern, URLResolver, path, include

from api.apps.users.views import RegisterView

urlpatterns: list[URLResolver | URLPattern] = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", RegisterView.as_view(), name="register"),
]
