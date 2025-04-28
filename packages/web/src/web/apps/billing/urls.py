from django.urls import URLResolver, URLPattern, path

from web.apps.billing.views import BillingView

urlpatterns: list[URLResolver | URLPattern] = [
    path("", BillingView.as_view(), name="billing"),
]
