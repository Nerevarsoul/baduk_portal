from django.contrib import admin

from dynamic_raw_id.admin import DynamicRawIDMixin
from dynamic_raw_id.filters import DynamicRawIDFilter
from rangefilter.filter import DateRangeFilter

from tsumego.models import Tsumego, TsumegoResult


@admin.register(Tsumego)
class TsumegoAdmin(admin.ModelAdmin):
    list_display = ('date', 'kind', 'level', )
    list_filter = (('date', DateRangeFilter), 'kind', 'level')


@admin.register(TsumegoResult)
class TsumegoResultAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    list_display = ('tsumego', 'user', 'status', )
    list_filter = ('status', ('user', DynamicRawIDFilter),)
    search_fields = ('user__username',)
    list_select_related = ('user',)
    dynamic_raw_id_fields = ('user',)
