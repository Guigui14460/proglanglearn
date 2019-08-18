from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class ArticleQuerySet(models.QuerySet):
    def last_articles(self, number):
        return self.published_articles()[:number]

    def published_articles(self):
        return self.filter(published=True, timestamp__lte=timezone.now())

    def send_email(self):
        return self.filter(email_send=False, published=True, timestamp__lte=timezone.now())


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def get_last_articles(self, number):
        return self.get_queryset().last_articles(number)

    def get_published_articles(self):
        return self.get_queryset().published_articles()

    def get_send_email_article(self):
        return self.get_queryset().send_email()

    def search(self, query):
        if settings.SEARCH_TYPE == 'multiple':
            return self.search_multiple(query)
        elif settings.SEARCH_TYPE == 'simple':
            return self.search_simple(query)
        return self.none()

    def search_simple(self, query):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(content__icontains=query))
            qs = qs.filter(or_lookup)
        return qs

    def search_multiple(self, query):
        qs = self.none()
        if query is not None:
            for word in query.split():
                or_lookup = (Q(title__icontains=word) |
                             Q(content__icontains=word))
                qs = qs | self.get_queryset().filter(or_lookup)
            qs.distinct()
        return qs
