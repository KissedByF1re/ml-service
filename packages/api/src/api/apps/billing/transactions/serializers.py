from rest_framework import serializers

from api.apps.billing.models import Transaction


class TransactionSerializer(serializers.ModelSerializer[Transaction]):
    class Meta:
        model = Transaction
        fields = ("value", "type")
