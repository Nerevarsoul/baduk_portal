from django_tables2 import SingleTableView

from .models import TsumegoResult
from .tables import TsumegoResultTable


class TsumegoResultListView(SingleTableView):
    model = TsumegoResult
    table_class = TsumegoResultTable
    template_name = 'tsumego_result_list.html'
