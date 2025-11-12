from django.db import models
from rooms.models import BaseModel


class Client(BaseModel):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Электронная почта'
    )

    @property
    def name(self):
        """Возвращает полное имя"""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name',)

    def __str__(self):
        return f'{self.name} ({self.phone})'
