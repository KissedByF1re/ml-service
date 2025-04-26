import typing

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from api.apps.billing.models import Balance, Transaction
from api.apps.billing.balance.serializers import BalanceSerializer
from api.apps.billing.transactions.use_cases.create_transaction import CreateTransactionUseCase
from api.apps.users.models import User


class BalanceView(RetrieveUpdateAPIView[Balance]):
    serializer_class = BalanceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Balance]:
        user = typing.cast(User, self.request.user)
        return Balance.objects.filter(user=user)

    def get_object(self) -> Balance:
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer: BaseSerializer[Balance]) -> None:
        original_balance = self.get_object()
        balance = serializer.save()

        difference = balance.value - original_balance.value
        if difference > 0:
            type_ = Transaction.Type.deposit
        else:
            type_ = Transaction.Type.debit

        CreateTransactionUseCase.execute(balance.user_id, value=difference, type_=type_)
