import itertools

import django_tables2 as tables
from .models import Tournament


class TournamentTable(tables.Table):
    class Meta:
        model = Tournament
        template_name = 'django_tables2/bootstrap.html'
        fields = ('row_number', 'player',)
        order_by = '-total'

    row_number = tables.Column(empty_values=(), verbose_name='№', orderable=False)
    player = tables.Column(verbose_name='Игрок')
    wins = tables.Column(verbose_name='Победы')
    total = tables.Column(verbose_name='Очки')

    def __init__(self, *args, **kwargs):
        new_data = []
        extra_columns = []

        for participant in kwargs['data'][0].participants.all():
            new_data.append({'player': participant.user.username, 'all_games': 0, 'wins': 0})
            # extra_columns.append((participant.user.username, tables.Column()))

        for game in kwargs['data'][0].games.all():
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

        for d in new_data:
            if d['all_games']:
                d['total'] = round(d['wins'] / d['all_games'] + d['wins'] * 0.04, 2)
                extra_columns.append((d['player'], tables.Column()))
            else:
                d['total'] = 0

        kwargs['data'] = new_data
        kwargs['extra_columns'] = extra_columns
        super().__init__(*args, **kwargs)

    def render_row_number(self):
        self.row_number = getattr(self, 'row_number', itertools.count())
        return next(self.row_number) + 1
