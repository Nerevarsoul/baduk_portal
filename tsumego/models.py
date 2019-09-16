from django.db import models

from accounts.models import User


class Tsumego(models.Model):
    TSUMEGO_TYPE = (
        ('life and death', 'жизнь и смерть'),
        ('fuseki', 'фусеки'),
        ('yose', 'йосе'),
        ('position', 'позиционка'),
    )

    LEVEL_CHOICES = (
        ('0', 'для всех'),
        ('1', 'для начинающих'),
        ('2', 'для старшей группы'),
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    date = models.DateField(verbose_name='Дата публикации')
    number = models.IntegerField(verbose_name='Номер')
    kind = models.CharField(
        choices=TSUMEGO_TYPE,
        max_length=20
    )
    level = models.CharField(
        verbose_name='Уровень',
        choices=LEVEL_CHOICES,
        max_length=2
    )

    def __str__(self):
        return f'Задача №{self.number} за {self.date}'


class TsumegoResult(models.Model):
    STATUS_CHOICES = (
        ('done', 'решена'),
        ('failed', 'с ошибкой'),
    )

    class Meta:
        verbose_name = 'Результат задачи'
        verbose_name_plural = 'Результаты задач'

    tsumego = models.ForeignKey(
        Tsumego,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=10
    )
