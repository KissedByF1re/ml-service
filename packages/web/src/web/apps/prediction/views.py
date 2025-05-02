from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.handlers.wsgi import WSGIRequest


class PredictionView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, "prediction/prediction.html", context={"domain": settings.BE_DOMAIN})
