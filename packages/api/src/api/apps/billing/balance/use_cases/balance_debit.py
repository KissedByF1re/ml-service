from django.db.models import F

from api.apps.billing.models import Balance


class BalanceDebitUseCase:
    @staticmethod
    def execute(user_id: int, value: int) -> None:
        Balance.objects.filter(user_id=user_id).update(value=F("value") - value)
