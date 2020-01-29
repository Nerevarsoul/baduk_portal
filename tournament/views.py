from django.views.generic import ListView
from django_tables2 import SingleTableView

from tournament.models import Tournament, Title
from tournament.tables import TournamentTable, TournamentLigaTable


__all__ = ('SingleTournamentView', 'LastTournamentByTitleView', 'TournamentTitlesListView',)


class BaseTournamentView(SingleTableView):

    template_name = 'tournament_table.html'
    table_pagination = False

    def get_table_class(self):

        title = Title.objects.get(id=self.kwargs.get('title_id'))
        if title.kind == Title.KIND_CHOICES[1][0]:
            table_class = TournamentTable
        else:
            table_class = TournamentLigaTable

        return table_class


class SingleTournamentView(BaseTournamentView):

    def get_queryset(self):
        return Tournament.objects.details(self.kwargs.get('id'))


class LastTournamentByTitleView(BaseTournamentView):

    def get_queryset(self):
        return Tournament.objects.last_by_title(self.kwargs.get('title_id'))


class TournamentTitlesListView(ListView):
    model = Title
    template_name = 'tournament_title_list.html'
