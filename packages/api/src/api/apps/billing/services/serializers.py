from rest_framework import serializers

from api.apps.billing.models import Service


class ServiceSerializer(serializers.ModelSerializer[Service]):
    class Meta:
        model = Service
        fields = ("id", "name", "model", "price")
