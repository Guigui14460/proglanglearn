from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserExperienceJournal(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("utilisateur associé"))
    experience = models.PositiveIntegerField(
        default=0, verbose_name=_("expérience"))
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date/heure"))

    class Meta:
        verbose_name = _("journal d'expérience utilisateur")
        verbose_name_plural = _("journaux d'expérience utilisateur")

    def __str__(self):
        return f"{self.user.username} - {self.timestamp} : {self.experience}"

    def save(self, *args, **kwargs):
        self.timestamp = now()
        super().save(*args, **kwargs)
