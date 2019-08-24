from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Poll, Item, Vote


class PollItemInline(admin.TabularInline):
    model = Item
    extra = 0
    max_num = 15


class PollAdmin(ImportExportModelAdmin):
    list_display = ('title', 'date', 'end_date', 'votes', 'is_published')
    inlines = [PollItemInline, ]
    list_filter = ['is_published', 'date', 'end_date']


class VoteAdmin(ImportExportModelAdmin):
    list_display = ('poll', 'ip', 'user', 'datetime')
    list_filter = ['datetime', 'poll']


admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)
