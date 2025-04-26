from django.urls import URLPattern, URLResolver, path

from api.apps.billing.views import BalanceView

urlpatterns: list[URLResolver | URLPattern] = [
    path("balance/", BalanceView.as_view(), name="balance"),
]
