from django.db.models import QuerySet, Count, Q, Manager


class TsumegoResultQuerySet(QuerySet):

    def list(self):
        return self.select_related('user', 'tsumego')

    def list_by_user(self):
        return self.list().filter(status='done')\
            .values('user__username').annotate(total=Count('user')).order_by('-total')


class TsumegoResultManager(Manager):

    def get_queryset(self):
        return TsumegoResultQuerySet(self.model, using=self._db)

    def list(self):
        return self.get_queryset().list()

    def list_by_user(self):
        return self.get_queryset().list_by_user()
