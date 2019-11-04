from django.db.models import QuerySet, Manager


class TournamentQuerySet(QuerySet):

    def details(self, id):
        return self.filter(id=id).prefetch_related('participants', 'games', 'participants__user')


class TournamentManager(Manager):

    def get_queryset(self):
        return TournamentQuerySet(self.model, using=self._db)

    def details(self, id):
        return self.get_queryset().details(id)
