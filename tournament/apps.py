from django.apps import AppConfig

import django_rq


class TournamentConfig(AppConfig):
    name = 'tournament'
    verbose_name = 'Турниры'

    def ready(self):
        from .tasks import parse_games_from_kgs

        scheduler = django_rq.get_scheduler('default')

        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.cron('0 * * * *', func=parse_games_from_kgs, repeat=None)
