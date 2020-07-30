from django.contrib import admin
from .models import Account, TimeTable
from . import models

admin.site.register(Account)


class TimeTableItemInline(admin.TabularInline):
    model = models.TimeTableItem
    ordering = ('start_time',)
    extra = 1


@admin.register(models.TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = [ 'day']
    inlines = [TimeTableItemInline]
