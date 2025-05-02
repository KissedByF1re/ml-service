from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from api.apps.billing.models import Service
from api.apps.billing.services.serializers import ServiceSerializer


class ServicesView(ListAPIView[Service]):
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Service]:
        return Service.objects.filter()


class ServiceView(RetrieveAPIView[Service]):
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Service]:
        return Service.objects.filter()
