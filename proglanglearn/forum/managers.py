from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class SubjectQuerySet(models.QuerySet):
    def last_subjects(self, number):
        return self.published_subjects()[:number]

    def published_subjects(self):
        return self.filter(timestamp__lte=timezone.now())


class SubjectManager(models.Manager):
    def get_queryset(self):
        return SubjectQuerySet(self.model, using=self._db)

    def get_last_subjects(self, number):
        return self.get_queryset().last_subjects(number)

    def get_published_subjects(self):
        return self.get_queryset().published_subjects()

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
