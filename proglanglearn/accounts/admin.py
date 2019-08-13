from django.conf import settings
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Education, Experience, Profile, ProfileReport


def strike_profile(modeladmin, request, queryset):
    queryset.update(verified=True, to_strike=True, striked=True)
    for report in queryset:
        report.profile.strike += 1
        report.profile.save()
        if int(report.profile.strike) >= settings.MAX_STRIKE:
            strike_msg = _("Vous êtes définitivement banni de ProgLangLearn, c'est-à-dire que l'accès à votre compte n'est plus possible. Aucun recours sera possible comme stipulé dans nos conditions générales d'utilisation.")
        else:
            strike_msg = _("Il ne vous reste que %(nb)d signalements pour être définitivement banni et perdre votre compte ProgLangLearn") % {
                'nb': settings.MAX_STRIKE - report.comment.author.profile.strike}
        subject = _("Votre profil a été signalé")
        message = _("Votre profil a été signalé le %(date)s car il comporte des irrégularités. Veuillez les corriger au plus vite. %(strike_msg)s") % {
            'date': report.timestamp, 'strike_msg': strike_msg}
        msg = EmailMultiAlternatives(
            subject, message, "ProgLangLearn", to=[report.profile.user.email])
        msg.send()


strike_profile.short_description = _("Striker le profil")


class EducationAdmin(ImportExportModelAdmin):
    pass


class ExperienceAdmin(ImportExportModelAdmin):
    pass


class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user', 'level', 'strike', 'email_notification', 'is_dev',
                    'is_student', 'is_teacher')
    ordering = ('user', 'level', 'strike', 'is_dev',
                'is_student', 'is_teacher')
    search_fields = ['user']
    list_filter = ['strike', 'is_dev', 'is_student',
                   'is_teacher', 'strike', 'email_notification', 'level']
    empty_value_display = _("Inconnu")
    fieldsets = (
        (_("Espace critique"), {'fields': ('strike',
                                           'email_confirmed', 'email_notification')}),
        (_("Informations générales"), {'fields': (
            'user', 'image', 'biography', 'links', 'languages_learnt', 'is_dev', 'is_student', 'is_teacher', 'github_username', 'country')}),
        (_("Options avancées"), {'fields': ('level', 'level_experience')})
    )


class ProfileReportAdmin(ImportExportModelAdmin):
    list_display = ('profile', 'timestamp', 'verified', 'to_strike', 'striked')
    list_filter = ('timestamp', 'verified', 'to_strike', 'striked')
    ordering = ('timestamp',)
    search_field = ['profile', 'profile__user__username']
    actions = [strike_profile]


admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileReport, ProfileReportAdmin)
