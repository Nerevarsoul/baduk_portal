import itertools

import django_tables2 as tables
from .models import Tournament


__all__ = (
    'TournamentTable', 'TournamentLigaTable', 'TournamentListTable', 'TournamentInfoTable',
    'TournamentGroupLigaTable',
)


class BaseTournamentTable(tables.Table):

    def render_row_number(self):
        self.row_number = getattr(self, 'row_number', itertools.count())
        return next(self.row_number) + 1


class TournamentTable(BaseTournamentTable):
    class Meta:
        model = Tournament
        template_name = 'django_tables2/bootstrap.html'
        fields = ('row_number', 'player',)
        order_by = ('-total', '-all_games')
        row_attrs = {
            'class': lambda record: 'font-weight-bold' if record['all_games'] > 3 else ''
        }

    row_number = tables.Column(empty_values=(), verbose_name='№', orderable=False)
    player = tables.Column(verbose_name='Игрок')
    all_games = tables.Column(verbose_name='Игры')
    wins = tables.Column(verbose_name='Победы')
    total = tables.Column(verbose_name='Очки')

    def __init__(self, *args, **kwargs):
        new_data = []
        extra_columns = []

        for participant in kwargs['data'].participants.all():
            new_data.append(
                {
                    'player': participant.user.username,
                    'all_games': 0,
                    'wins': 0
                }
            )

        for game in kwargs['data'].games.all():
            if game.result == 'white':
                winner = game.white_player.user.username
                looser = game.black_player.user.username
            else:
                winner = game.black_player.user.username
                looser = game.white_player.user.username
            for col in new_data:
                if col['player'] == winner:
                    col[looser] = 1
                    col['all_games'] += 1
                    col['wins'] += 1
                if col['player'] == looser:
                    col[winner] = 0
                    col['all_games'] += 1

        title_holder = kwargs['data'].participants.filter(title_holder=True)

        for d in new_data:
            if d['all_games']:
                d['total'] = round(
                    d['wins'] / d['all_games'] +
                    d['wins'] * kwargs['data'].point_for_win +
                    d['all_games'] * kwargs['data'].point_for_game,
                    2
                )
                extra_columns.append((d['player'], tables.Column()))
            else:
                d['total'] = 0

            if title_holder and d['player'] == title_holder[0].user.username:
                d['player'] += ' 👑'

        kwargs['data'] = new_data
        kwargs['extra_columns'] = extra_columns
        super().__init__(*args, **kwargs)

    def render_row_number(self):
        self.row_number = getattr(self, 'row_number', itertools.count())
        return next(self.row_number) + 1


class TournamentLigaTable(BaseTournamentTable):
    class Meta:
        model = Tournament
        template_name = 'django_tables2/bootstrap.html'
        fields = ('row_number', 'player',)
        order_by = ('-score',)

    row_number = tables.Column(empty_values=(), verbose_name='№', orderable=False)
    player = tables.Column(verbose_name='Игрок')
    level = tables.Column(verbose_name='Рейтинг')
    points = tables.Column(verbose_name='Очки')
    score = tables.Column(verbose_name='Счет')

    def __init__(self, *args, **kwargs):
        new_data = []

        for participant in kwargs['data'].participants.all():
            new_data.append(
                {
                    'player': participant.user.username,
                    'level': participant.level,
                    'points': 0,
                    'score': participant.start_points
                }
            )

        kwargs['data'] = new_data

        super().__init__(*args, **kwargs)
        

class TournamentGroupLigaTable(BaseTournamentTable):
    class Meta:
        model = Tournament
        template_name = 'django_tables2/bootstrap.html'
        fields = ('row_number',)

    row_number = tables.Column(empty_values=(), verbose_name='№', orderable=False)


class TournamentListTable(tables.Table):
    class Meta:
        model = Tournament
        template_name = 'django_tables2/bootstrap.html'
        fields = ('row_number', 'name', 'start_date', 'end_date', 'info_url', 'table_url',)
        order_by = ('-start_date',)

    row_number = tables.Column(empty_values=(), verbose_name='№', orderable=False)
    info_url = tables.TemplateColumn('<a href="info/{{record.id}}">Инфо</a>', verbose_name='')
    table_url = tables.TemplateColumn('<a href="tables/{{record.id}}">Таблица</a>', verbose_name='')

    def render_row_number(self):
        self.row_number = getattr(self, 'row_number', itertools.count())
        return next(self.row_number) + 1


class TournamentInfoTable(tables.Table):
    class Meta:
        model = Tournament
        template_name = 'django_tables2/bootstrap.html'
        fields = ('row_number', )

    row_number = tables.Column(empty_values=(), verbose_name='№', orderable=False)
    player = tables.Column(verbose_name='Игрок')
    rank_string = tables.Column(verbose_name='Ранг')

    def __init__(self, *args, **kwargs):
        new_data = []

        for participant in kwargs['data'].participants.all():
            new_data.append(
                {
                    'player': participant.user.username,
                    'rank_string': participant.get_rank_string,
                    'rank_int': participant.get_rank_int
                }
            )

        kwargs['data'] = sorted(new_data, key=lambda x: x['rank_int'], reverse=True)
        super().__init__(*args, **kwargs)

    def render_row_number(self):
        self.row_number = getattr(self, 'row_number', itertools.count())
        return next(self.row_number) + 1
