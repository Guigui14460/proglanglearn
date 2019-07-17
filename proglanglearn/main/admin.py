from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Comment, CommentReport, Language, Tag, User


def give_staff_status(modeladmin, request, queryset):
    queryset.update(is_staff=True)


give_staff_status.short_description = _("Donner le statut d'administrateur")


def strike_comment(modeladmin, request, queryset):
    queryset.update(verified=True, striked=True)


strike_comment.short_description = _("Striker le commentaire")


class CommentAdmin(ImportExportModelAdmin):
    pass


class CommentReportAdmin(ImportExportModelAdmin):
    list_display = ('comment', 'type_alert', 'verified', 'striked')
    list_filter = ['verified', 'striked']
    empty_value_display = _("Inconnu")
    list_editable = ['verified', 'striked']
    actions = [strike_comment]


class LanguageAdmin(ImportExportModelAdmin):
    pass


class TagAdmin(ImportExportModelAdmin):
    pass


class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_editable = ['is_staff']
    actions = [give_staff_status]


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
