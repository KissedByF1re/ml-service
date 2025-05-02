from django.urls import URLResolver, URLPattern, path

from web.apps.users.views import LoginView, RegisterView

urlpatterns: list[URLResolver | URLPattern] = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
]
