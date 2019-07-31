from django.db import models
from django.db.models import Q
from django.utils import timezone


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
