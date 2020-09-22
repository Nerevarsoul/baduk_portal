from django.contrib import admin

from .models import *


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_filter = ('kind',)
    list_display = (
        'name', 'kind',
    )


@admin.register(Tag)
class VideoAdmin(admin.ModelAdmin):
    pass
