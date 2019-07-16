from django.contrib import admin
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Course, Tutorial


from main.utils import get_thumbnail_preview


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
    list_display = ('title', 'get_author_profile', get_thumbnail_preview, 'published_date',
                    'old_price', 'new_price')
    ordering = ('published_date', 'old_price', 'new_price')
    search_fields = ['title']
    fields = ('author', 'title', 'thumbnail', get_thumbnail_preview, 'content_introduction',
              'difficulty', 'languages', 'tags', 'pdf', 'published_date', 'old_price', 'new_price')

    empty_value_display = _("Inconnu")
    readonly_fields = [get_thumbnail_preview]
    inlines = [TutorialInline]

    def get_author_profile(self, obj=None):
        if obj.pk:
            return mark_safe(f"<a href='{reverse('main:index')}'>{obj.author.username}</a>")
        return _("Enregistrez pour avoir le lien de l'auteur du cours")


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
