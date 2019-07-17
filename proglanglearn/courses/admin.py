from datetime import datetime, date

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Course, Tutorial


from main.utils import get_thumbnail_preview


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
                return queryset.filter(published_date__gte=date(int(year), 1, 1), published_date__lte=date(int(year), 12, 31))


class TutorialInline(admin.StackedInline):
    model = Tutorial
    extra = 0
    fields = ('title', 'content', 'resources', 'experience')
    readonly_fields = ["get_edit_link"]

    def get_edit_link(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s' % (obj._meta.app_label,
                                           obj._meta.model_name), args=[str(obj.pk)])
            return mark_safe("<a href='{}'>{}</a>".format(url, _('Éditer le %s séparement') % obj._meta.verbose_name))
        return _('Enregistrez et continuez à éditer pour créer un lien')
    get_edit_link.short_description = _("Édit le lien")
    get_edit_link.allow_tags = True


class CourseAdmin(ImportExportModelAdmin):
    list_display = ('title', 'get_author_profile', get_thumbnail_preview, 'difficulty', 'published_date',
                    'old_price', 'new_price')
    ordering = ('published_date', 'old_price', 'new_price')
    search_fields = ['title']
    fields = ('author', 'title', 'thumbnail', get_thumbnail_preview, 'content_introduction',
              'difficulty', 'languages', 'tags', 'pdf', 'published_date', 'old_price', 'new_price')
    list_filter = ['published_date', YearListFilter]
    empty_value_display = _("Inconnu")
    readonly_fields = [get_thumbnail_preview]
    inlines = [TutorialInline]
    list_editable = ['difficulty']

    def get_author_profile(self, obj=None):
        if obj.pk:
            return mark_safe(f"<a href='{reverse('main:index')}'>{obj.author.username}</a>")
        return _("Enregistrez pour avoir le lien de l'auteur du cours")
    get_author_profile.allow_tags = True
    get_author_profile.short_description = _("Auteur")


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


admin.site.register(Course, CourseAdmin)
admin.site.register(Tutorial, TutorialAdmin)
