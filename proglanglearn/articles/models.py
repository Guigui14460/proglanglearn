from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete, pre_save
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _

from tinymce.models import HTMLField

from main.models import Language, Tag, Comment
from main.utils import unique_slug_generator


User = settings.AUTH_USER_MODEL


class ArticleQuerySet(models.QuerySet):
    def last_articles(self, number):
        return self.published_articles()[:number]

    def published_articles(self):
        return self.filter(timestamp__lte=timezone.now())

    def search(self, query):
        return self.filter((Q(title__icontains=query) | Q(content__icontains=query)).distinct())


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def get_last_articles(self, number):
        return self.get_queryset().last_articles(number)

    def get_published_articles(self):
        return self.get_queryset().published_articles()

    def search(self, query):
        return self.get_queryset().search(query)


class Article(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("Auteur"), related_name='articles')
    title = models.CharField(
        max_length=150, verbose_name=_("Titre de l'article"))
    slug = models.SlugField(verbose_name=_(
        "URL d'accès"), blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='blog_thumbnail/', verbose_name=_("Vignette/vidéo d'article"))
    languages = models.ManyToManyField(
        Language, verbose_name=_("Langages utilisés"), blank=True, related_name='article')
    tags = models.ManyToManyField(
        Tag, verbose_name=_("Catégories"), blank=True, related_name='article')
    content = HTMLField(
        verbose_name=_("Contenu"))
    timestamp = models.DateField(
        verbose_name=_("Date de publication"))
    last_modification = models.DateField(
        verbose_name=_("Dernière modification"))
    views = models.BigIntegerField(verbose_name=_(
        "Nombre de vues"), blank=True, default=0)

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
        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id).count()


def submission_article_delete(sender, instance, **kwargs):
    if instance.thumbnail != None:
        instance.thumbnail.delete(save=False)


def pre_save_article_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


post_delete.connect(submission_article_delete, sender=Article)
pre_save.connect(pre_save_article_receiver, sender=Article)
