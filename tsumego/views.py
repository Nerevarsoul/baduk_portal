from datetime import date

from django_tables2 import SingleTableView

from .models import TsumegoResult
from .tables import *


class TsumegoResultListView(SingleTableView):
    model = TsumegoResult
    table_class = TsumegoResultTable
    template_name = 'tsumego_result_list.html'
    table_pagination = False

    def get_queryset(self):
        year = self.kwargs.get('year') if self.kwargs.get('year') else date.today().year
        month = self.kwargs.get('month') if self.kwargs.get('month') else date.today().month
        return TsumegoResult.objects.list_by_user(year, month)


class TsumegoAllResultListView(TsumegoResultListView):
    table_class = TsumegoAllResultTable
    queryset = TsumegoResult.objects.list()
