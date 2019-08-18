from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class LanguageQuerySet(models.QuerySet):
    pass


class LanguageManager(models.Manager):
    def get_queryset(self):
        return LanguageQuerySet(self.model, using=self._db)

    def search(self, query):
        if settings.SEARCH_TYPE == 'multiple':
            return self.search_multiple(query)
        elif settings.SEARCH_TYPE == 'simple':
            return self.search_simple(query)
        return self.none()

    def search_simple(self, query):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(content__icontains=query))
            qs = qs.filter(or_lookup)
        return qs

    def search_multiple(self, query):
        qs = self.none()
        if query is not None:
            for word in query.split():
                or_lookup = (Q(name__icontains=word) |
                             Q(content__icontains=word))
                qs = qs | self.get_queryset().filter(or_lookup)
            qs.distinct()
        return qs


class TagQuerySet(models.QuerySet):
    pass


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def search(self, query):
        if settings.SEARCH_TYPE == 'multiple':
            return self.search_multiple(query)
        elif settings.SEARCH_TYPE == 'simple':
            return self.search_simple(query)
        return self.none()

    def search_simple(self, query):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(content__icontains=query))
            qs = qs.filter(or_lookup)
        return qs

    def search_multiple(self, query):
        qs = self.none()
        if query is not None:
            for word in query.split():
                or_lookup = (Q(name__icontains=word) |
                             Q(content__icontains=word))
                qs = qs | self.get_queryset().filter(or_lookup)
            qs.distinct()
        return qs

