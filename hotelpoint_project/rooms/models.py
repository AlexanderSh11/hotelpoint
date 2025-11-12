from django.db import models


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract = True


class RoomCategory(BaseModel):
    title = models.CharField(
        max_length=100,
        null=False,
        verbose_name='Категория'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание категории'
    )

    class Meta:
        verbose_name = 'категория номера'
        verbose_name_plural = 'Категории номеров'

    def __str__(self):
        return self.title
    

class Room(BaseModel):
    ROOM_TYPE_CHOICES = [
        ('1', 'Одноместный'),
        ('2', 'Двухместный'),
        ('3', 'Трёхместный'),
    ]

    number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Номер комнаты'
    )
    room_type = models.CharField(
        max_length=1,
        choices=ROOM_TYPE_CHOICES,
        verbose_name='Тип комнаты'
    )
    category = models.ForeignKey(
        RoomCategory,
        on_delete=models.PROTECT,
        related_name='rooms',
        verbose_name='Категория'
    )
    base_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Базовая цена (руб.)'
    )

    class Meta:
        verbose_name = 'номер'
        verbose_name_plural = 'Номера'

    def __str__(self):
        return f'Номер {self.number} ({self.room_type} {self.category})'
    

class RoomPrice(BaseModel):
    WEEKDAY_CHOICES = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]

    weekday = models.CharField(
        unique=True,
        max_length=3,
        choices=WEEKDAY_CHOICES,
        verbose_name='День недели'
    )
    percentage = models.IntegerField(
        default=100,
        verbose_name='Процент от базовой цены (%)',
        help_text='От 0 (бесплатно) до 200 (удвоенная базовая цена)'
    )

    class Meta:
        verbose_name = 'цена за день недели'
        verbose_name_plural = 'Цены по дням недели'
        ordering = ['weekday']

    def __str__(self):
        return f'{self.get_weekday_display()}: {self.percentage}% от базовой цены'