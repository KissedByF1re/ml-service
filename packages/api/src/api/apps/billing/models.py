from django.contrib.auth import get_user_model
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class Balance(models.Model):
    class Meta(TypedModelMeta):
        db_table = "balance"
        verbose_name = "баланс"
        verbose_name_plural = "балансы"

    class Currency(models.TextChoices):
        RUB = "RUB", "RUB"

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="balance",
        verbose_name="Пользователь",
    )
    value = models.IntegerField(default=0, verbose_name="Сумма (в копейках)")
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.RUB, verbose_name="Валюта")

    def __str__(self) -> str:
        return f"{self.user.username} – {self.value / 100} {self.currency}"


class Transaction(models.Model):
    class Meta(TypedModelMeta):
        db_table = "transactions"
        verbose_name = "транзакции"
        verbose_name_plural = "транзакции"

    class Type(models.TextChoices):
        deposit = "deposit", "Пополнение"
        debit = "debit", "Списание"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Пользователь",
    )
    value = models.IntegerField(verbose_name="Сумма (в копейках)")
    type = models.CharField(max_length=7, choices=Type.choices, verbose_name="Валюта")

    def __str__(self) -> str:
        return f"{self.user.username} – {self.type} {self.value}"
