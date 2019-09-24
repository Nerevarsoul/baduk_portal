import itertools

import django_tables2 as tables
from .models import TsumegoResult


class TsumegoResultTable(tables.Table):
    class Meta:
        model = TsumegoResult
        template_name = 'django_tables2/bootstrap.html'
        fields = ('row_number', 'username', 'total',)

    row_number = tables.Column(empty_values=(), verbose_name='№')
    total = tables.Column(verbose_name='Решено')
    username = tables.Column(verbose_name='Имя', accessor='user__username')

    def render_row_number(self):
        self.row_number = getattr(self, 'row_number', itertools.count())
        return next(self.row_number) + 1
