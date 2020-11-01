from copy import deepcopy

from django.views.generic import TemplateView
from django_tables2 import SingleTableView

from tournament.models import Tournament, Title
from tournament.tables import *


__all__ = (
    'SingleTournamentView', 'LastTournamentByTitleView', 'TournamentTitlesListView',
    'TournamentInfoView', 'VueTournamentView',
)


class VueTournamentView(TemplateView):
    template_name = 'vue_tournament_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['table_data'] = {
            'Группа А': [
                {'name': 'Andrey', 'age': 12},
                {'name': 'Oleg', 'age': 16},
            ],
            'Группа Б': [
                {'name': 'Jorg', 'age': 22},
                {'name': 'Finn', 'age': 46},
            ],
            'Группа В': [
                {'name': 'Bert', 'age': 112},
                {'name': 'Vaomi', 'age': 6},
            ],
            'Группа Г': [
                {'name': 'Carl', 'age': 17},
                {'name': 'Bill', 'age': 76},
            ],
        }
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
