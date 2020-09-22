from django.db.models import QuerySet, Manager


class TournamentQuerySet(QuerySet):

    def details(self, tournament_id):
        return self.filter(id=tournament_id).prefetch_related(
            'participants', 'games', 'participants__user'
        ).first()

    def last_by_title(self, title_id):
        return self.filter(title=title_id, is_active=True).prefetch_related(
            'participants', 'games', 'participants__user'
        ).order_by('-id').first()


class TournamentManager(Manager):

    def get_queryset(self):
        return TournamentQuerySet(self.model, using=self._db)

    def details(self, tournament_id):
        return self.get_queryset().details(tournament_id)

    def last_by_title(self, title_id):
        return self.get_queryset().last_by_title(title_id)
