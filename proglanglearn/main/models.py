from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from .signals import comment_signal


ALERT_CHOICES = (
    ('A', _('Harcèlement')),
    ('B', _('Discriminations physiques, racistes, sexistes')),
    ('C', _('Incitations ou apologie du terrorisme')),
    ('D', _('Incitations à la violence et à la haine')),
    ('E', _('Autre (explications demandées)'))
)


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']
    ip_address = models.GenericIPAddressField(
        verbose_name=_("Adresse IP"), null=True, blank=True)


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name=_("Nom du langage de programmation"))

    class Meta:
        verbose_name = _("Langage")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name=_("Nom du tag"))

    class Meta:
        verbose_name = _("Catégorie")

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments', verbose_name=_("Auteur"))
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Modèle de l'objet"))
    object_id = models.PositiveIntegerField(
        verbose_name=_("Identifiant de l'objet"))
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField(verbose_name=_("Commentaire ou réponse"))
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Date de publication"))

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Commentaire")
        verbose_name_plural = _("Commentaires")

    def __str__(self):
        c_type = ContentType.objects.get_for_model(self)
        if c_type == self.content_type:
            return f"Comment by {self.author} : {self.content[:20]}"
        else:
            return f"Reply by {self.author} : {self.content[:20]}"

    @property
    def is_parent(self):
        c_type = ContentType.objects.get_for_model(self)
        return c_type != self.content_type

    @property
    def children(self):
        c_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=c_type, object_id=self.id).order_by('timestamp')

    @property
    def get_report_url(self):
        return reverse('main:report-comment', kwargs={'comment_id': self.id})

    def comments_instance(self, instance):
        c_type = ContentType.objects.get_for_model(instance)
        return Comment.objects.filter(content_type=c_type, object_id=instance.id)


def comment_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    new_obj = Comment.objects.create(
        author=request.user,
        content_type=c_type,
        object_id=instance.id,
        content=request.POST.get('content')
    )


comment_signal.connect(comment_receiver)


class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name='reports', verbose_name=_("Commentaire reporté"))
    alerter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("Signaleur"))
    type_alert = models.CharField(
        max_length=1, choices=ALERT_CHOICES, verbose_name=_("Type de signalement"))
    content_alert = models.TextField(verbose_name=_(
        "Contenu du signalement"), null=True, blank=True)

    class Meta:
        verbose_name = _("Signalement de commentaire")
        verbose_name_plural = _("Signalements de commentaire")

    def __str__(self):
        return f"{self.comment.id} reported by {self.alerter.username}"
