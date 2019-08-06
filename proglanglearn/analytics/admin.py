from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import UserExperienceJournal


class UserExperienceJournalAdmin(ImportExportModelAdmin):
    ordering = ('-timestamp',)
    search_fields = ['user__username']


admin.site.register(UserExperienceJournal, UserExperienceJournalAdmin)
