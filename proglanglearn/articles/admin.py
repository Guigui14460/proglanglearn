from datetime import datetime, date

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from main.utils import get_thumbnail_preview
from .models import Article


YEAR_REF = 2019


def send_email_article(model_admin, request, queryset):
    for article in queryset:
        article.published = True
        article.save()
    messages.success(request, _(
        "Article publiés avec succès"))


send_email_article.short_description = _(
    "Publication des articles (les rendre visibles si la date est dépassée + autorisation d'envoi d'email notificatif)")


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


class ArticleAdmin(ImportExportModelAdmin):
    list_display = ('title', 'get_author_profile', get_thumbnail_preview, 'timestamp', 'last_modification',
                    'published', 'email_send')
    ordering = ('-timestamp', '-last_modification', 'published', 'email_send')
    search_fields = ['title', 'author__username']
    fields = ('author', 'title', 'thumbnail', get_thumbnail_preview, 'content',
              'languages', 'tags', 'timestamp', 'last_modification')
    list_filter = ['timestamp', 'last_modification',
                   'published', 'email_send', YearListFilter]
    empty_value_display = _("Inconnu")
    readonly_fields = [get_thumbnail_preview]
    list_editable = ['published', 'email_send']
    actions = [send_email_article]

    def get_author_profile(self, obj=None):
        if obj.pk:
            return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(obj.author.profile._meta.app_label, obj.author.profile._meta.model_name), args=(obj.author.profile.pk,))}'>{obj.author.username}</a>")
        return _("Enregistrez pour avoir le lien de l'auteur de l'article")
    get_author_profile.allow_tags = True
    get_author_profile.short_description = _("Auteur")


admin.site.register(Article, ArticleAdmin)
