from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class BillingView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, "billing/billing.html", context={"domain": settings.BE_DOMAIN})
