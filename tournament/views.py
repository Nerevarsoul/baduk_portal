from django.views.generic import ListView
from django_tables2 import SingleTableView

from tournament.models import Tournament, Title
from tournament.tables import TournamentTable


__all__ = ('SingleTournamentView', 'LastTournamentByTitleView', 'TournamentTitlesListView',)


class SingleTournamentView(SingleTableView):
    table_class = TournamentTable
    template_name = 'tournament_table.html'
    table_pagination = False

    def get_queryset(self):
        return Tournament.objects.details(self.kwargs.get('id'))


class LastTournamentByTitleView(SingleTableView):
    table_class = TournamentTable
    template_name = 'tournament_table.html'
    table_pagination = False

    def get_queryset(self):
        return Tournament.objects.last_by_title(self.kwargs.get('title_id'))


class TournamentTitlesListView(ListView):
    model = Title
    template_name = 'tournament_title_list.html'
