from django_tables2 import SingleTableView

from tournament.models import Tournament
from tournament.tables import TournamentTable


class SingleTournamentView(SingleTableView):
    table_class = TournamentTable
    template_name = 'tournament_table.html'
    table_pagination = False

    def get_queryset(self):
        return Tournament.objects.details(self.kwargs.get('id'))
