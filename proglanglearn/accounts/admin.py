from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'strike', 'is_dev',
                    'is_student', 'is_teacher')
    list_filter = ('user', 'level', 'strike', 'is_dev',
                   'is_student', 'is_teacher')
    ordering = ('user', 'level', 'strike', 'is_dev',
                   'is_student', 'is_teacher')
    search_fields = ['user']

    empty_value_display = _("Inconnu")
    fieldsets = (
        (_("Espace critique"), {'fields': ('strike',)}),
        (_("Informations générales"), {'fields': (
            ('user', 'image'), ('is_dev', 'is_student', 'is_teacher'), 'country')}),
        (_("Options avancées"), {'fields': ('level', 'experience')})
    )


admin.site.unregister(Group)
admin.site.register(Profile, ProfileAdmin)
