from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session

from import_export.admin import ImportExportModelAdmin

from .models import Comment, CommentReport, Language, Tag, User


class CommentAdmin(ImportExportModelAdmin):
    pass


class CommentReportAdmin(ImportExportModelAdmin):
    pass


class LanguageAdmin(ImportExportModelAdmin):
    pass


class TagAdmin(ImportExportModelAdmin):
    pass


class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    pass


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
