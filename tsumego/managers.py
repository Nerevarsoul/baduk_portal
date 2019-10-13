from datetime import date

from django.db.models import QuerySet, Count, Q, Manager


class TsumegoResultQuerySet(QuerySet):

    def list(self):
        return self.select_related('user', 'tsumego')

    def list_by_user(self, year: int, month: int):
        return self.list().filter(
            status='done', tsumego__date__year=year, tsumego__date__month=month
        ).values('user__username').annotate(
            total=Count('user'),
            first_total=Count('user', filter=Q(tsumego__date__lte=date(year, month, 15))),
            second_total=Count('user', filter=Q(tsumego__date__gt=date(year, month, 15))),
        ).order_by('-total')


class TsumegoResultManager(Manager):

    def get_queryset(self):
        return TsumegoResultQuerySet(self.model, using=self._db)

    def list(self):
        return self.get_queryset().list()

    def list_by_user(self, year: int, month: int):
        return self.get_queryset().list_by_user(year, month)
