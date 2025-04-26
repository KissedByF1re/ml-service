from api.apps.billing.models import Transaction


class CreateTransactionUseCase:
    @staticmethod
    def execute(user_id: int, value: int, type_: Transaction.Type) -> Transaction:
        transaction = Transaction.objects.create(user_id=user_id, value=value, type=type_)
        return transaction
