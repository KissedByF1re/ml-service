from django.contrib.auth.models import AbstractUser
from django_stubs_ext.db.models import TypedModelMeta


class User(AbstractUser):
    class Meta(TypedModelMeta):
        db_table = "users"
        managed = False
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}" if self.first_name or self.last_name else self.username
