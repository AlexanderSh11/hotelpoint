from django.db import models
from rooms.models import Room, BaseModel
from clients.models import Client


class Booking(BaseModel):
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Номер'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Клиент'
    )
    check_in = models.DateField(
        verbose_name='Дата заезда'
    )
    check_out = models.DateField(
        verbose_name='Дата выезда'
    )
    has_child_bed = models.BooleanField(
        default=False,
        verbose_name='Нужна детская кровать',
        help_text='Установить детскую кровать в номере при бронировании'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Общая стоимость (руб.)'
    )
    is_canceled = models.BooleanField(
        default=False,
        verbose_name='Бронирование отменено'
    )
    
    @property
    def duration(self):
        """Количество ночей проживания."""
        return (self.check_out - self.check_in).days

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Бронь {self.client} - {self.room} ({self.check_in}-{self.check_out})'
