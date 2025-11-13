from decimal import ROUND_HALF_UP, Decimal
from django.db import models
from rooms.models import Room, BaseModel, RoomPrice
from clients.models import Client
from django.core.exceptions import ValidationError
from django.utils import timezone


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

    def calculate_total_price(self):
        """Рассчитать общую стоимость с учетом процентов по дням недели и с учетом скидки за продолжительность"""
        total = Decimal('0')
        current_date = self.check_in
        
        # Проходим по всем дням бронирования
        while current_date < self.check_out:
            price_percent = RoomPrice.objects.get(weekday=current_date.strftime('%a').lower())
            percentage = Decimal(price_percent.percentage) / Decimal('100')
            
            day_price = (self.room.base_price * percentage).quantize(Decimal('0.01'))
            total += day_price
            
            current_date += timezone.timedelta(days=1)
        
        # Если больше 7 ночей - общая скидка 20%
        if self.duration > 7:
            total *= Decimal('0.80')
        # Если больше 5 ночей - общая скидка 15%
        elif self.duration > 5:
            total *= Decimal('0.85')
        # Если больше 3 ночей - общая скидка 10%
        elif self.duration > 3:
            total *= Decimal('0.90')

        return total.quantize(Decimal('0.01'))

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("Дата выезда должна быть позже даты заезда.")

        # Проверка на пересечение с другими бронированиями
        overlapping = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("Этот номер уже забронирован на выбранные даты.")

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.room:
            self.total_price = self.calculate_total_price()

        self.full_clean()
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Бронь {self.client} - {self.room} ({self.check_in}-{self.check_out})'
