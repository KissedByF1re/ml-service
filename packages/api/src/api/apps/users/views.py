import typing

from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_framework.serializers import BaseSerializer

from api.apps.billing.models import Balance
from api.apps.users.models import User


class RegisterView(BaseRegisterView):  # type: ignore[misc]
    def perform_create(self, serializer: BaseSerializer[User]) -> User:
        user = typing.cast(User, super().perform_create(serializer=serializer))
        Balance.objects.create(user=user)
        return user
