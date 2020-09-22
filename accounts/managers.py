from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import QuerySet, Manager


class SubscriptionQuerySet(QuerySet):

    def get_subscriptions_by_date(self, year, month):
        date_start = date(year=year, month=month, day=1)
        date_end = date_start + relativedelta(months=1) - timedelta(days=1)
        return self.select_related('user').filter(period__gte=date_start, period__lte=date_end)


class SubscriptionManager(Manager):

    def get_queryset(self):
        return SubscriptionQuerySet(self.model, using=self._db)

    def get_subscriptions_by_date(self, year: int, month: int):
        return self.get_queryset().get_subscriptions_by_date(year, month)
