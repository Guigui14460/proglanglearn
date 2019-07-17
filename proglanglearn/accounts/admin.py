from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Education, Experience, Profile


class EducationAdmin(ImportExportModelAdmin):
    pass


class ExperienceAdmin(ImportExportModelAdmin):
    pass


class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user', 'level', 'strike', 'is_dev',
                    'is_student', 'is_teacher')
    list_filter = ('level', 'strike', 'is_dev',
                   'is_student', 'is_teacher')
    ordering = ('user', 'level', 'strike', 'is_dev',
                'is_student', 'is_teacher')
    search_fields = ['user']
    list_filter = ['strike', 'level']
    empty_value_display = _("Inconnu")
    fieldsets = (
        (_("Espace critique"), {'fields': ('strike', 'email_confirmed')}),
        (_("Informations générales"), {'fields': (
            'user', 'image', 'biography', 'links', 'languages_learnt', 'is_dev', 'is_student', 'is_teacher', 'github_username', 'country')}),
        (_("Options avancées"), {'fields': ('level', 'level_experience')})
    )


admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Profile, ProfileAdmin)
