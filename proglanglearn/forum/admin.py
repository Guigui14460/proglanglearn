from datetime import date

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Subject, SubjectAnswer


YEAR_REF = 2019


class YearListFilter(admin.SimpleListFilter):
    title = _('année de publication')

    parameter_name = 'year'

    def lookups(self, request, model_admin):
        today_year = int(date.today().year)
        return ((str(i), str(i)) for i in range(YEAR_REF, today_year + 1))

    def queryset(self, request, queryset):
        years = [str(i) for i in range(
            YEAR_REF, int(date.today().year) + 1)]
        for year in years:
            if self.value() == year:
                return queryset.filter(timestamp__gte=date(int(year), 1, 1), timestamp__lte=date(int(year), 12, 31))


class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('title', 'get_author_link', 'timestamp', 'closed')
    search_fields = ['title', 'user__username']
    fields = ['user', 'title', 'content', 'languages', 'closed', 'views']
    list_filter = ['timestamp', 'closed', YearListFilter]
    empty_value_display = _("Inconnu")

    def get_author_link(self, obj=None):
        if obj.pk:
            return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(obj.user._meta.app_label, obj.user._meta.model_name), args=(obj.user.pk,))}'>{obj.user.username}</a>")
        return _("Enregistrez pour avoir le lien de l'auteur du cours")
    get_author_link.allow_tags = True
    get_author_link.short_description = _("Auteur")


class SubjectAnswerAdmin(ImportExportModelAdmin):
    list_display = ('subject', 'get_author_link', 'timestamp', 'best_answer')
    search_fields = ['subject', 'user__username']
    fields = ['user', 'subject', 'content',
              'best_answer', 'likes']
    list_filter = ['timestamp', 'best_answer', YearListFilter]
    empty_value_display = _("Inconnu")

    def get_author_link(self, obj=None):
        if obj.pk:
            return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(obj.user._meta.app_label, obj.user._meta.model_name), args=(obj.user.pk,))}'>{obj.user.username}</a>")
        return _("Enregistrez pour avoir le lien de l'auteur du cours")
    get_author_link.allow_tags = True
    get_author_link.short_description = _("Auteur")


admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectAnswer, SubjectAnswerAdmin)
