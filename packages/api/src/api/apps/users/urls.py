from django.urls import URLPattern, URLResolver, path, include

urlpatterns: list[URLResolver | URLPattern] = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
]
