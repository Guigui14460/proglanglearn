from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from .managers import PublishedManager


User = get_user_model()


class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250, verbose_name=_("question"))
    date = models.DateField(auto_now_add=True, verbose_name=_("date"))
    end_date = models.DateField(
        null=True, blank=True, verbose_name=_("date de fin"))
    is_published = models.BooleanField(
        default=True, blank=True, verbose_name=_("est publié"))

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-date', '-end_date', 'title']
        verbose_name = _("sondage")
        verbose_name_plural = _("sondages")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('polls:poll', kwargs={'poll_pk': self.pk})

    def get_vote_url(self):
        return reverse('polls:poll_ajax_vote', kwargs={'poll_pk': self.pk})

    def get_result_url(self):
        return reverse('polls:poll_result', kwargs={'poll_pk': self.pk})

    def get_vote_count(self):
        return Vote.objects.filter(poll=self).count()
    get_vote_count.short_description = _("Total de vote")

    def get_cookie_name(self):
        return f"poll_{self.pk}"


class Item(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='items', verbose_name=_("sondage asscoié"))
    value = models.CharField(max_length=200, verbose_name=_("valeur"))
    position = models.SmallIntegerField(default=0, verbose_name=_("position"))

    class Meta:
        ordering = ['poll', 'position']
        verbose_name = _("réponse de sondage")
        verbose_name_plural = _("réponses de sondage")

    def __str__(self):
        return self.value

    def get_vote_count(self):
        return Vote.objects.filter(item=self).count()


class Vote(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, verbose_name=_("sondage associé"))
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name=_("valeur votée"))
    ip = models.GenericIPAddressField(
        verbose_name=_("adresse IP de l'utilisateur"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             blank=True, null=True, verbose_name=_("utilisateur associé"))
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['poll', '-datetime']
        verbose_name = _("vote de sondage")
        verbose_name_plural = _("votes de sondage")

    def __str__(self):
        try:
            return self.user.username
        except:
            return f"{self.ip}"
