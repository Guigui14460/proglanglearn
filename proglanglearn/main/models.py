from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

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
        verbose_name=_("adresse IP"), null=True, blank=True)


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name=_("nom du langage de programmation"))
    slug = models.SlugField(null=True, blank=True,
                            verbose_name=_("URL d'accès"))
    image = models.ImageField(
        upload_to='languages_tags/', verbose_name=_("logo"), null=True, blank=True)
    content = HTMLField(verbose_name=_(
        "description du langage"), null=True, blank=True)

    class Meta:
        verbose_name = _("langage de programmation")
        verbose_name_plural = _("langages de programmation")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:language_tag', slug=self.slug)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name=_("nom de la catégorie"))
    slug = models.SlugField(null=True, blank=True,
                            verbose_name=_("URL d'accès"))
    image = models.ImageField(upload_to='languages_tags/',
                              verbose_name=_("illustration"), null=True, blank=True)
    content = HTMLField(verbose_name=_(
        "description de la catégorie"), null=True, blank=True)

    class Meta:
        verbose_name = _("catégorie")
        verbose_name_plural = _("catégories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:language_tag', slug=self.slug)


def pre_save_language_tag_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_language_tag_receiver, sender=Language)
pre_save.connect(pre_save_language_tag_receiver, sender=Tag)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments', verbose_name=_("auteur"))
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("modèle de l'objet"))
    object_id = models.PositiveIntegerField(
        verbose_name=_("identifiant de l'objet"))
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField(verbose_name=_("commentaire ou réponse"))
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date de publication"))
    reported = models.BooleanField(default=False, verbose_name=_("reporté"))

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("commentaire")
        verbose_name_plural = _("commentaires")

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
        return Comment.objects.filter(content_type=c_type, object_id=self.id, reported=False).order_by('timestamp')

    @property
    def get_report_url(self):
        return reverse('main:report-comment', kwargs={'comment_id': self.id})

    def comments_instance(self, instance):
        c_type = ContentType.objects.get_for_model(instance)
        return Comment.objects.filter(content_type=c_type, object_id=instance.id, reported=False)

    @property
    def get_delete_url(self):
        return reverse('main:delete-comment', kwargs={'comment_id': self.id})


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
                                related_name='reports', verbose_name=_("commentaire reporté"))
    alerter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("signaleur"))
    type_alert = models.CharField(
        max_length=1, choices=ALERT_CHOICES, verbose_name=_("type de signalement"))
    content_alert = models.TextField(verbose_name=_(
        "contenu du signalement"), null=True, blank=True)
    verified = models.BooleanField(verbose_name=_("vérifié"), default=False)
    to_strike = models.BooleanField(default=False, verbose_name=_("à striker"))
    striked = models.BooleanField(verbose_name=_("striké"), default=False)

    class Meta:
        verbose_name = _("signalement de commentaire")
        verbose_name_plural = _("signalements de commentaire")

    def __str__(self):
        return f"{self.comment.id} reported by {self.alerter.username if self.alerter is not None else 'Unknown'}"
