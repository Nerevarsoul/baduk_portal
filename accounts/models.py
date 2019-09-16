import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    kgs_username = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    SUBSCRIPTIONS_TYPE = (
        ('tsumego', 'задачи'),
        ('league', 'лига'),
        ('theory', 'теория'),
        ('handicap league', 'форовая лига'),
        ('special', 'специальное'),
        ('OGS', 'ОГС'),
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    kind = models.CharField(
        verbose_name='Тип',
        choices=SUBSCRIPTIONS_TYPE,
        max_length=20
    )
    period = models.DateField(verbose_name='Месяц действия')
    user = models.ForeignKey(
        User,
        verbose_name='Участник',
        on_delete=models.CASCADE
    )
