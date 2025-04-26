from rest_framework import serializers

from api.apps.billing.models import Balance


class BalanceSerializer(serializers.ModelSerializer[Balance]):
    class Meta:
        model = Balance
        fields = ("value", "currency")
