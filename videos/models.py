from django.db import models

from model_utils.models import TimeStampedModel


class Video(TimeStampedModel):
    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    KIND_CHOICES = (
        ('lecture', 'лекция'),
        ('stream', 'стрим'),
        ('tsumego_answer', 'ответ на задачу'),
        ('review', 'разбор'),
    )

    name = models.CharField(verbose_name='Название', max_length=150)
    kind = models.CharField(
        verbose_name='Тип',
        choices=KIND_CHOICES,
        default=KIND_CHOICES[1][0],
        max_length=20
    )
    url = models.URLField(verbose_name='Ссылка')
    sgf = models.FileField(verbose_name='СГФ файл', blank=True, null=True)


