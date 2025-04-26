import typing

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from api.apps.billing.models import Balance
from api.apps.billing.serializers import BalanceSerializer
from api.apps.users.models import User


class BalanceView(RetrieveUpdateAPIView[Balance], CreateModelMixin):
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

    def perform_create(self, serializer: BaseSerializer[Balance]) -> None:
        user = typing.cast(User, self.request.user)
        data = serializer.data
        Balance.objects.create(user=user, **data)

    def post(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        user = typing.cast(User, self.request.user)
        balance = Balance.objects.filter(user=user)
        if balance:
            from rest_framework.response import Response

            return Response({"error": "Balance already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)
