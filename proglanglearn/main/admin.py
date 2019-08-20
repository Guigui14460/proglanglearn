from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Comment, CommentReport, EmailAdminNotificationForUsers, Language, Tag, User


def give_staff_status(modeladmin, request, queryset):
    queryset.update(is_staff=True)


give_staff_status.short_description = _("Donner le statut d'administrateur")


def strike_comment(modeladmin, request, queryset):
    queryset.update(verified=True, to_strike=True, striked=True)
    for report in queryset:
        report.comment.reported = True
        report.comment.save()
        report.comment.author.profile.strike += 1
        report.comment.author.profile.save()
        if int(report.comment.author.profile.strike) >= settings.MAX_STRIKE:
            strike_msg = _("Vous êtes définitivement banni de ProgLangLearn, c'est-à-dire que l'accès à votre compte n'est plus possible. Aucun recours sera possible comme stipulé dans nos conditions générales d'utilisation.")
        else:
            strike_msg = _("Il ne vous reste que %(nb)d signalements pour être définitivement banni et perdre votre compte ProgLangLearn") % {
                'nb': settings.MAX_STRIKE - report.comment.author.profile.strike}
        subject = _("Un de vos commentaire a été signalé")
        message = _("Votre commentaire datant du %(date)s a été signalé.\nLe type de signalement est : %(type)s."
                    "\nVotre commentaire ne sera plus visible. %(strike_msg)s") % {'date': report.comment.timestamp, 'type': report.get_type_alert_display(), 'strike_msg': strike_msg}
        msg = EmailMultiAlternatives(
            subject, message, "ProgLangLearn", to=[report.comment.author.email])
        msg.send()


strike_comment.short_description = _("Striker le commentaire")


class CommentAdmin(ImportExportModelAdmin):
    pass


class CommentReportAdmin(ImportExportModelAdmin):
    list_display = ('comment', 'type_alert',
                    'verified', 'to_strike', 'striked')
    list_filter = ['verified', 'to_strike', 'striked']
    empty_value_display = _("Inconnu")
    list_editable = ['verified', 'to_strike', 'striked']
    actions = [strike_comment]


class EmailAdminNotificationForUsersAdmin(ImportExportModelAdmin):
    fields = ['subject_fr', 'subject_en', 'body_fr', 'body_en']


class LanguageAdmin(ImportExportModelAdmin):
    fields = ['name', 'name_fr', 'name_en',
              'image', 'content_fr', 'content_en']


class TagAdmin(ImportExportModelAdmin):
    fields = ['name', 'name_fr', 'name_en',
              'image', 'content_fr', 'content_en']


class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_editable = ['is_staff']
    actions = [give_staff_status]


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
admin.site.register(EmailAdminNotificationForUsers,
                    EmailAdminNotificationForUsersAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
