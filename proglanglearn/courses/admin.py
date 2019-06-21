from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Course, Section, Tutorial


class CourseAdmin(ImportExportModelAdmin):
    pass


class SectionAdmin(ImportExportModelAdmin):
    pass


class TutorialAdmin(ImportExportModelAdmin):
    list_display = ('title', 'published_date')
    ordering = ('published_date',)
    search_fields = ['title']

    empty_value_display = _("Inconnu")
    fieldsets = (
        (_("Info générales"), {'fields': ('title', 'content')}),
        (_("Info complémentaires"), {
         'fields': ('experience', 'published_date')})
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Tutorial, TutorialAdmin)
