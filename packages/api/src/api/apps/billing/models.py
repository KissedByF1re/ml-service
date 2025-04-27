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

    user_id: int
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    def __str__(self) -> str:
        return f"{self.user.username} – {self.type} {self.value}"


class Service(models.Model):
    class Meta(TypedModelMeta):
        db_table = "services"
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

    name = models.CharField(verbose_name="Название")
    model = models.CharField(verbose_name="Модель")
    price = models.IntegerField(verbose_name="Цена (в копейках)")

    def __str__(self) -> str:
        return self.name


class ServiceOrder(models.Model):
    class Meta(TypedModelMeta):
        db_table = "service_orders"
        verbose_name = "заказ услуги"
        verbose_name_plural = "заказы услуг"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="service_orders",
        verbose_name="Пользователь",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Услуга",
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="service_orders",
        verbose_name="Транзакция",
    )
    price = models.IntegerField(verbose_name="Цена (в копейках)")
    is_provided = models.BooleanField(default=False, verbose_name="Предоставлена ли услуга?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    def __str__(self) -> str:
        return f"{self.user.username} – {self.service.name}"
