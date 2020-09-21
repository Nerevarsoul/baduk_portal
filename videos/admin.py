from django.contrib import admin

from .models import *


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_filter = ('kind',)
    list_display = (
        'name', 'kind',
    )

    @staticmethod
    def get_tournament(instance):
        return instance.tournament.name

    @staticmethod
    def get_rank(instance):
        return instance.get_rank_string
