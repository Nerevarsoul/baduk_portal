import django_tables2 as tables
from .models import TsumegoResult


class TsumegoResultTable(tables.Table):
    class Meta:
        model = TsumegoResult
        template_name = 'django_tables2/bootstrap.html'
        fields = ('status', 'user', 'tsumego',)
