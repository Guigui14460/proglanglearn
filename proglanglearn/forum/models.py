from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

from main.models import Language, Tag
from .managers import SubjectManager


User = get_user_model()


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name=_("utilisateur associé"))
    title = models.CharField(max_length=200, verbose_name=_("titre du sujet"))
    content = HTMLField(verbose_name=_("contenu"))
    languages = models.ManyToManyField(
        Language, verbose_name=_("langages utilisés"), related_name='subject')
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date de création"))
    closed = models.BooleanField(default=False, verbose_name=_("fermé"))
    views = models.PositiveIntegerField(default=0, verbose_name=_("vues"))

    objects = SubjectManager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("sujet")
        verbose_name_plural = _("sujets")

    def __str__(self):
        try:
            return f"{self.title} - {self.user.username}"
        except:
            return f"{self.title} - Unknown"

    def get_absolute_url(self):
        return reverse('forum:subject-detail', kwargs={'id': self.id})

    def get_favorite_url(self):
        return reverse('forum:subject-favorite', kwargs={'id': self.id})

    def get_answer(self):
        return self.answers.all()

    def is_closed(self):
        return self.answers.filter(best_answer=True).exists()


class SubjectAnswer(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                related_name='answers', verbose_name=_("sujet associé"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='subject_answers', verbose_name=_("utilisateur associé"))
    content = HTMLField(verbose_name=_("réponse"))
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date de publication"))
    likes = models.ManyToManyField(User, verbose_name=_("j'aimes"))
    best_answer = models.BooleanField(
        default=False, verbose_name=_("meilleure réponse"))

    class Meta:
        ordering = ['best_answer', 'timestamp']
        verbose_name = _("réponse de sujet")
        verbose_name_plural = _("réponses de sujet")

    def __str__(self):
        return f"{self.user.username} -> {self.subject}"

    def get_like_url(self):
        return reverse('forum:subject-answer-like', kwargs={'subject_id': self.subject.id, 'answer_id': self.id})
