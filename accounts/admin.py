from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


@admin.register(User)
class UserAdmin(UserAdmin):
    UserAdmin.fieldsets += (None, {
            'classes': ('wide',),
            'fields': ('kgs_username',),
        }),


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
