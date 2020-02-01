from django_tables2 import SingleTableView

from tournament.models import Tournament, Title
from tournament.tables import *


__all__ = (
    'SingleTournamentView', 'LastTournamentByTitleView', 'TournamentTitlesListView',
    'TournamentInfoView',
)


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
