from django.contrib import admin
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Answer, Question, Quiz, Sitting


def reset_quiz(modeladmin, request, queryset):
    queryset.update(random_order=False, single_attempt=False)


reset_quiz.short_description = _("Réinitialiser les valeurs booléennes")


def make_quiz_random(modeladmin, request, queryset):
    queryset.update(random_order=True)


make_quiz_random.short_description = _("Afficher les questions aléatoirement")


def make_single_attempt(modeladmin, request, queryset):
    queryset.update(single_attempt=True)


make_single_attempt.short_description = _("Droit qu'à un seul essai")


def make_question_random(modeladmin, request, queryset):
    queryset.update(random_answer_display=True)


make_question_random.short_description = _(
    "Afficher les réponses aléatoirement")


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 5
    fields = ('question', 'content', 'correct')


class AnswerAdmin(ImportExportModelAdmin):
    list_display = ('get_content_safe', 'get_question_link', 'correct')
    search_fields = ['content', 'question__question_text',
                     'question__quiz__title']
    empty_value_display = _("Inconnu")
    list_filter = ['correct']
    fieldsets = (
        (_("Info générales"), {
         'fields': ('question', 'content', 'correct')}),
    )

    def get_question_link(self, obj=None):
        if obj.pk:
            return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(obj.question._meta.app_label, obj.question._meta.model_name), args=(obj.question.pk,))}'>{obj.question.question_text[:20]}</a>")
        return _("Enregistrez pour avoir le lien de la question")
    get_question_link.allow_tags = True
    get_question_link.short_description = _("Question")

    def get_content_safe(self, obj=None):
        if obj.pk:
            return mark_safe(obj.content)
        return _("Enregistrez pour avoir le lien de l'objet")
    get_content_safe.allow_tags = True
    get_content_safe.short_description = _("Contenu")


class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('get_question_text_safe',
                    'get_quiz_link', 'random_answer_display', 'experience')
    search_fields = ['question_text', 'quiz__title']
    empty_value_display = _("Inconnu")
    list_filter = ['random_answer_display', 'experience']
    fieldsets = (
        (_("Info générales"), {
         'fields': ('quiz', 'question_text', 'explanation')}),
        (_("Info complémentaires"), {
         'fields': ('random_answer_display', 'experience')})
    )
    inlines = [AnswerInline]
    actions = [make_question_random]

    def get_quiz_link(self, obj=None):
        if obj.pk:
            quiz = Quiz.objects.filter(questions__id=obj.id)
            if len(quiz) > 0:
                quiz = quiz.first()
                return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(quiz._meta.app_label, quiz._meta.model_name), args=(quiz.pk,))}'>{quiz.title}</a>")
        return _("Enregistrez pour avoir le lien du quiz")
    get_quiz_link.allow_tags = True
    get_quiz_link.short_description = _("Quiz")

    def get_question_text_safe(self, obj=None):
        if obj.pk:
            return mark_safe(obj.question_text)
        return _("Enregistrez pour avoir le lien de l'objet")
    get_question_text_safe.allow_tags = True
    get_question_text_safe.short_description = _("Question")


class QuizAdmin(ImportExportModelAdmin):
    list_display = ('title', 'get_course_link',
                    'random_order', 'single_attempt')
    search_fields = ['title', 'course__title']
    list_filter = ['random_order', 'single_attempt']
    empty_value_display = _("Inconnu")
    fieldsets = (
        (_("Info générales"), {
         'fields': ('course', 'title', 'description')}),
        (_("Info complémentaires"), {
         'fields': ('random_order', 'single_attempt')})
    )
    actions = [reset_quiz, make_quiz_random, make_single_attempt]

    def get_course_link(self, obj=None):
        if obj.pk:
            return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(obj.course._meta.app_label, obj.course._meta.model_name), args=(obj.course.pk,))}'>{obj.course.title}</a>")
        return _("Enregistrez pour avoir le lien du cours")
    get_course_link.allow_tags = True
    get_course_link.short_description = _("Cours")


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
