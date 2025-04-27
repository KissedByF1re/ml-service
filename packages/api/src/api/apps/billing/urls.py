from django.urls import URLPattern, URLResolver, path

from api.apps.billing.balance.views import BalanceView, BalanceDepositView
from api.apps.billing.service_orders.views import ServiceOrderView
from api.apps.billing.services.views import ServicesView, ServiceView
from api.apps.billing.transactions.views import TransactionsView

urlpatterns: list[URLResolver | URLPattern] = [
    path("balance/", BalanceView.as_view(), name="balance"),
    path("balance/deposit/", BalanceDepositView.as_view(), name="balance-deposit"),
    path("transactions/", TransactionsView.as_view(), name="transactions"),
    path("services/", ServicesView.as_view(), name="services"),
    path("services/<int:pk>/", ServiceView.as_view(), name="service"),
    path("services/order/", ServiceOrderView.as_view(), name="service-order"),
]
