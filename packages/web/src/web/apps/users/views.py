from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.core.handlers.wsgi import WSGIRequest


class RegisterView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(to="prediction")

        return render(request, "users/register.html", context={"domain": settings.BE_DOMAIN})


class LoginView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(to="prediction")

        return render(request, "users/login.html", context={"domain": settings.BE_DOMAIN})
