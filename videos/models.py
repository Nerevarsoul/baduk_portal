from django.db import models

from model_utils.models import TimeStampedModel


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    name = models.CharField(verbose_name='Имя', max_length=50)


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
    sgf = models.FileField(verbose_name='СГФ файл', upload_to='sgf', blank=True, null=True)
    date = models.DateField(verbose_name='Дата')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', related_name='tag_videos')
