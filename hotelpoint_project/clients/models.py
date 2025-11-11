from django.db import models
from rooms.models import BaseModel


class Client(BaseModel):
    name = models.CharField(
        max_length=150,
        verbose_name='ФИО клиента'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Электронная почта'
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.phone})'
