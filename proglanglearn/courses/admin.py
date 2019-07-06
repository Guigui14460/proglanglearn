from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Course, Tutorial, TutorialComment, TutorialCommentReport


class CourseAdmin(ImportExportModelAdmin):
    list_display = ('title', 'author', 'published_date',
                    'old_price', 'new_price')
    ordering = ('published_date', 'old_price', 'new_price')
    search_fields = ['title']

    empty_value_display = _("Inconnu")


class TutorialAdmin(ImportExportModelAdmin):
    list_display = ('title', 'course', 'published_date')
    ordering = ('published_date',)
    search_fields = ['title']

    empty_value_display = _("Inconnu")
    fieldsets = (
        (_("Info générales"), {'fields': ('course', 'title', 'content')}),
        (_("Info complémentaires"), {
         'fields': ('resources', 'experience', 'published_date')})
    )


class TutorialCommentAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(TutorialComment, TutorialCommentAdmin)
admin.site.register(TutorialCommentReport)
