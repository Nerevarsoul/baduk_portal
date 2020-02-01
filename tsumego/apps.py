from django.apps import AppConfig

import django_rq


class TsumegoConfig(AppConfig):
    name = 'tsumego'
    verbose_name = 'Задачи'

    def ready(self):
        from .tasks import parse_current_tsumego

        # scheduler = django_rq.get_scheduler('default')

        # scheduler.cron('0 * * * *', func=parse_current_tsumego, repeat=None)
