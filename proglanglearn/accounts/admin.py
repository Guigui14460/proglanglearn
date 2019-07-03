from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Profile, Education, Experience, Tag, Language

User = get_user_model()


class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    pass


class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user', 'level', 'strike', 'is_dev',
                    'is_student', 'is_teacher')
    list_filter = ('level', 'strike', 'is_dev',
                   'is_student', 'is_teacher')
    ordering = ('user', 'level', 'strike', 'is_dev',
                'is_student', 'is_teacher')
    search_fields = ['user']

    empty_value_display = _("Inconnu")
    fieldsets = (
        (_("Espace critique"), {'fields': ('strike', 'email_confirmed')}),
        (_("Informations générales"), {'fields': (
            'user', 'image', 'biography', 'links', 'languages_learnt', 'is_dev', 'is_student', 'is_teacher', 'github_username', 'country')}),
        (_("Options avancées"), {'fields': ('level', 'level_experience')})
    )


class ExperienceAdmin(ImportExportModelAdmin):
    pass


class EducationAdmin(ImportExportModelAdmin):
    pass


class TagAdmin(ImportExportModelAdmin):
    pass


class LanguageAdmin(ImportExportModelAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Language, LanguageAdmin)
