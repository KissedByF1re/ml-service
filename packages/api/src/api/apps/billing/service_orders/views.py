import typing

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from api.apps.billing.models import ServiceOrder
from api.apps.billing.service_orders.serializers import ServiceOrderCreateSerializer, ServiceOrderSerializer
from api.apps.users.models import User


class ServiceOrderView(CreateAPIView[ServiceOrder]):
    serializer_class = ServiceOrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[ServiceOrder]:
        return ServiceOrder.objects.filter()

    def create(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, user_id=request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: BaseSerializer[ServiceOrder], **kwargs: typing.Any) -> None:
        serializer.save(**kwargs)


class ServiceOrdersView(ListAPIView[ServiceOrder]):
    serializer_class = ServiceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[ServiceOrder]:
        user = typing.cast(User, self.request.user)
        return ServiceOrder.objects.filter(user=user)

    def get_object(self) -> ServiceOrder:
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj
