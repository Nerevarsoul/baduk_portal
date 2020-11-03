from collections import defaultdict
from copy import deepcopy

from django.views.generic import TemplateView, DetailView, ListView
from django_tables2 import SingleTableView

from tournament.models import Tournament, Title
from tournament.tables import *


__all__ = (
    'SingleTournamentView', 'LastTournamentByTitleView', 'TournamentTitlesListView',
    'TournamentInfoView', 'VueTournamentView',
)


class VueTournamentView(ListView):
    template_name = 'vue_tournament_table.html'

    def get_queryset(self):
        return Tournament.objects.details(self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        new_data = []
        # extra_columns = []

        tournament = context['object_list']

        for participant in tournament.participants.all():

            new_data.append(
                {
                    'player': participant.user.username,
                    'start_points': participant.start_points,
                    'all_games': 0,
                    'wins': 0
                }
            )

        for game in tournament.games.all():
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

        # for d in new_data:
        #     if d['all_games']:
        #         d['total'] = round(
        #             d['wins'] / d['all_games'] +
        #             d['wins'] * kwargs['data'].point_for_win +
        #             d['all_games'] * kwargs['data'].point_for_game,
        #             2
        #         )
        #         extra_columns.append((d['player'], tables.Column()))
        #     else:
        #         d['total'] = 0

        res = defaultdict(list)

        for i in new_data:
            res[i.pop('start_points')].append(i)

        for group in res:
            players = [p['player'] for p in res[group]]
            for row in res[group]:
                for p in players:
                    if p not in row:
                        row[p] = '-'

        context['object_list'] = res

        print(context['object_list'])

        return context


class BaseTournamentView(SingleTableView):

    template_name = 'tournament_table.html'
    table_pagination = False

    def get_table_by_title(self, title):
        if title.kind == Title.KIND_CHOICES[1][0]:
            table_class = TournamentTable
        elif title.kind == Title.KIND_CHOICES[2][0]:
            table_class = TournamentGroupLigaTable
        else:
            table_class = TournamentLigaTable

        return table_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if isinstance(context['table'], TournamentGroupLigaTable):
            context['tables'] = []
            start_points = {d['start_points'] for d in context['table'].data}
            start_points = sorted(tuple(start_points), reverse=True)
            for start_point in start_points:
                new_table = deepcopy(context['table'])
                new_table.data.data = [
                    d for d in new_table.data.data if d['start_points'] == start_point
                ]
                context['tables'].append(new_table)
        else:
            context['tables'] = [context['table']]
        return context


class SingleTournamentView(BaseTournamentView):

    def get_queryset(self):
        return Tournament.objects.details(self.kwargs.get('id'))

    def get_table_class(self):

        tour = Tournament.objects.get(id=self.kwargs.get('id'))

        return self.get_table_by_title(tour.title)


class LastTournamentByTitleView(BaseTournamentView):

    def get_queryset(self):
        return Tournament.objects.last_by_title(self.kwargs.get('title_id'))

    def get_table_class(self):

        title = Title.objects.get(id=self.kwargs.get('title_id'))

        return self.get_table_by_title(title)


class TournamentTitlesListView(SingleTableView):
    model = Tournament
    template_name = 'tournament_table.html'
    table_pagination = False
    table_class = TournamentListTable


class TournamentInfoView(SingleTableView):
    model = Tournament
    template_name = 'tournament_table.html'
    table_pagination = False
    table_class = TournamentInfoTable

    def get_queryset(self):
        return Tournament.objects.details(self.kwargs.get('id'))
