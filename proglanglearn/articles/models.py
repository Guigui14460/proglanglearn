from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

from main.models import Language, Tag, Comment
from main.utils import unique_slug_generator
from .managers import ArticleManager


User = settings.AUTH_USER_MODEL


class Article(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("auteur"), related_name='articles')
    title = models.CharField(
        max_length=150, verbose_name=_("titre de l'article"))
    slug = models.SlugField(verbose_name=_(
        "URL d'accès"), blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='blog_thumbnail/', verbose_name=_("vignette/vidéo d'article"))
    languages = models.ManyToManyField(
        Language, verbose_name=_("langages utilisés"), blank=True, related_name='article')
    tags = models.ManyToManyField(
        Tag, verbose_name=_("catégories"), blank=True, related_name='article')
    content = HTMLField(
        verbose_name=_("contenu"))
    published = models.BooleanField(default=False, verbose_name=_("publié"))
    email_send = models.BooleanField(
        default=False, verbose_name=_("emails envoyés"))
    timestamp = models.DateTimeField(
        verbose_name=_("date de publication"))
    last_modification = models.DateTimeField(
        verbose_name=_("dernière modification"))
    views = models.BigIntegerField(verbose_name=_(
        "nombre de vues"), blank=True, default=0)

    objects = ArticleManager()

    class Meta:
        ordering = ['-timestamp', '-views']
        verbose_name = _("article")

    def __str__(self):
        return f"{self.id} - {self.title} -> {self.author.username}"

    def save(self, *args, **kwargs):
        try:
            article = Article.objects.get(
                title=self.title, timestamp=self.timestamp)
            if article.thumbnail != self.thumbnail and article.thumbnail != None:
                article.thumbnail.delete(save=False)
        except:
            pass
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'article_slug': self.slug})

    def get_favorite_url(self):
        return reverse('articles:article-favorite', kwargs={'article_slug': self.slug})

    @property
    def get_comments_count(self):
        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id, reported=False).count()


def submission_article_delete(sender, instance, **kwargs):
    if instance.thumbnail != None:
        instance.thumbnail.delete(save=False)


def pre_save_article_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


post_delete.connect(submission_article_delete, sender=Article)
pre_save.connect(pre_save_article_receiver, sender=Article)
