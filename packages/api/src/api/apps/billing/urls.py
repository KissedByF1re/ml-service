from django.urls import URLPattern, URLResolver, path

from api.apps.billing.balance.views import BalanceView
from api.apps.billing.transactions.views import TransactionsView

urlpatterns: list[URLResolver | URLPattern] = [
    path("balance/", BalanceView.as_view(), name="balance"),
    path("transactions/", TransactionsView.as_view(), name="transactions"),
]
