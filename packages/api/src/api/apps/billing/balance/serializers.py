import typing

from rest_framework import serializers

from api.apps.billing.models import Balance


class BalanceSerializer(serializers.ModelSerializer[Balance]):
    class Meta:
        model = Balance
        fields = ("value", "currency")


class BalanceDepositSerializer(serializers.ModelSerializer[Balance]):
    amount = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Balance
        fields = ["value", "currency", "amount"]
        read_only_fields = ["value", "currency"]

    def update(self, instance: Balance, validated_data: dict[str, typing.Any]) -> Balance:
        amount = validated_data.pop("amount")
        instance.value += amount
        instance.save()
        return instance
