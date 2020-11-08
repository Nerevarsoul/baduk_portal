from django.db import models

from accounts.models import User
from tournament.managers import TournamentManager

__all__ = ('Title', 'Tournament', 'Participant', 'Game',)


class Title(models.Model):
    class Meta:
        verbose_name = 'Титул'
        verbose_name_plural = 'Титулы'

    KIND_CHOICES = (
        ('liga', 'лига'),
        ('all', 'круговая'),
        ('group', 'групповая лига'),
    )

    name = models.CharField(verbose_name='Название', max_length=150)
    kind = models.CharField(
        verbose_name='Тип',
        choices=KIND_CHOICES,
        default=KIND_CHOICES[1][0],
        max_length=10
    )
    tag = models.CharField(verbose_name='Тэг', max_length=150, blank=True, null=True)
    cron_string = models.CharField(
        verbose_name='Данные для авто создания турнира', max_length=20, blank=True, null=True
    )
    time_to_life = models.IntegerField(verbose_name='Продолжительность', blank=True, null=True)
    tour_number = models.IntegerField(verbose_name='Число туров', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    with_title_match = models.BooleanField(verbose_name='Матч за титул', blank=True, null=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'

    name = models.CharField(verbose_name='Название', max_length=150)
    title = models.ForeignKey(
        Title,
        verbose_name='Титул',
        on_delete=models.CASCADE,
    )
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    winner = models.ForeignKey(
        User,
        verbose_name='Победитель',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    tag = models.CharField(verbose_name='Тэг', max_length=150, blank=True, null=True)
    point_for_game = models.FloatField(verbose_name='Очки за партию', default=0)
    point_for_win = models.FloatField(verbose_name='Очки за победу', default=1)

    def __str__(self):
        return self.name

    objects = TournamentManager()


class Participant(models.Model):
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    RANK_CHOICES = (
        ('dan', 'дан'),
        ('kyu', 'кю'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    tournament = models.ForeignKey(
        Tournament,
        verbose_name='Турнир',
        on_delete=models.CASCADE,
        related_name='participants'
    )
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    rank = models.CharField(verbose_name='Ранг', max_length=3, blank=True, null=True)
    start_points = models.FloatField(verbose_name='Стартовые очки', blank=True, null=True)
    title_holder = models.BooleanField(verbose_name='Держатель титула', blank=True, null=True)
    challenger = models.BooleanField(verbose_name='Претендент', blank=True, null=True)
    group = models.IntegerField(verbose_name='Группа', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} ({self.tournament.name})'

    @property
    def get_rank_string(self):
        if self.level and self.rank:
            return f'{self.level} {self.rank}'
        return ''

    @property
    def get_rank_int(self):
        if self.level and self.rank:
            if self.rank == self.RANK_CHOICES[0][0]:
                return 30 + self.level
            else:
                return 30 - self.level
        return 0


class Game(models.Model):
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    STATUS_CHOICES = (
        ('done', 'окончена'),
        ('not played', 'не сыграна'),
    )

    RESULT_CHOICES = (
        ('black', 'b+'),
        ('white', 'w+'),
        ('jigo', '='),
    )

    tournament = models.ForeignKey(
        Tournament,
        verbose_name='Турнир',
        on_delete=models.CASCADE,
        related_name='games'
    )
    white_player = models.ForeignKey(
        Participant,
        verbose_name='Белый игрок',
        on_delete=models.CASCADE,
        related_name='white_user'
    )
    black_player = models.ForeignKey(
        Participant,
        verbose_name='Черный игрок',
        on_delete=models.CASCADE,
        related_name='black_user'
    )
    time_started = models.DateTimeField(verbose_name='Время начала партии', blank=True, null=True)
    status = models.CharField(
        verbose_name='Статус',
        choices=STATUS_CHOICES,
        max_length=10
    )
    result = models.CharField(
        verbose_name='Результат',
        choices=RESULT_CHOICES,
        max_length=10,
        blank=True,
        null=True
    )
    tour = models.IntegerField(verbose_name='№ тура', blank=True, null=True)
    handicap = models.IntegerField(verbose_name='Фора', blank=True, null=True)
    score = models.FloatField(verbose_name='Счет', blank=True, null=True)
    sgf = models.FileField(verbose_name='СГФ', blank=True, null=True)
    review_link = models.URLField(
        verbose_name='Ссылка на разбор', blank=True, null=True
    )

    def __str__(self):
        return f'{self.white_player.user.username} - {self.black_player.user.username}'
