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
    list_display = ('tsumego', 'user', 'status', 'get_level', 'get_kind',)
    list_filter = ('status', ('user', DynamicRawIDFilter), 'tsumego__level', 'tsumego__kind')
    search_fields = ('user__username',)
    list_select_related = ('user', 'tsumego')
    dynamic_raw_id_fields = ('user',)

    def get_level(self, obj):
        return obj.tsumego.get_level_display()
    get_level.short_description = 'Уровень задачи'

    def get_kind(self, obj):
        return obj.tsumego.get_kind_display()
    get_kind.short_description = 'Тип задачи'
