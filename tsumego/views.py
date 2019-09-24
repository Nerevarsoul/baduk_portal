from django_tables2 import SingleTableView

from .models import TsumegoResult
from .tables import TsumegoResultTable


class TsumegoResultListView(SingleTableView):
    queryset = TsumegoResult.objects.list_by_user()
    model = TsumegoResult
    table_class = TsumegoResultTable
    template_name = 'tsumego_result_list.html'
    table_pagination = False
