import typing

from rest_framework import serializers

from api.apps.billing.balance.use_cases.balance_debit import BalanceDebitUseCase
from api.apps.billing.models import ServiceOrder, Service, Transaction
from api.apps.billing.transactions.use_cases.create_transaction import CreateTransactionUseCase


class ServiceOrderCreateSerializer(serializers.ModelSerializer[ServiceOrder]):
    service_id = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), source="service", write_only=True)

    class Meta:
        model = ServiceOrder
        fields = ["id", "service_id"]

    def create(self, validated_data: dict[str, typing.Any]) -> ServiceOrder:
        service = validated_data["service"]
        user_id = validated_data["user_id"]
        BalanceDebitUseCase.execute(user_id=user_id, value=service.price)
        transaction = CreateTransactionUseCase.execute(
            user_id=user_id, value=service.price, type_=Transaction.Type.debit
        )
        service_order = ServiceOrder.objects.create(
            user_id=user_id, service=service, transaction=transaction, price=service.price
        )
        return service_order
