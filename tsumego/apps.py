from django.apps import AppConfig

import django_rq


class TsumegoConfig(AppConfig):
    name = 'tsumego'
    verbose_name = 'Задачи'

    def ready(self):
        from .tasks import parse_current_tsumego

        scheduler = django_rq.get_scheduler('default')

        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.cron('0 * * * *', func=parse_current_tsumego, repeat=None)
