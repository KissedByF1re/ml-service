import typing

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.apps.billing.models import Transaction
from api.apps.billing.transactions.serializers import TransactionSerializer
from api.apps.users.models import User


class TransactionsView(ListAPIView[Transaction]):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Transaction]:
        user = typing.cast(User, self.request.user)
        return Transaction.objects.filter(user=user)

    def get_object(self) -> Transaction:
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj
