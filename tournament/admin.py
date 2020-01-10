from django.contrib import admin

from .models import *


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_filter = (
        'tournament__name', 'title_holder', 'challenger',
    )
    list_select_related = ('user', 'tournament')
    list_display = ('user', 'get_tournament', 'title_holder', 'challenger',)

    @staticmethod
    def get_tournament(instance):
        return instance.tournament.name


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_filter = (
        'tournament__name',
    )
    list_display = (
        'tournament', 'white_player', 'black_player', 'time_started', 'result', 'score',
    )
    list_select_related = (
        'tournament', 'white_player', 'black_player', 'white_player__user', 'black_player__user',
    )
