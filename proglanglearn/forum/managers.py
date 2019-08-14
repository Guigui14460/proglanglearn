from django.db import models
from django.db.models import Q
from django.utils import timezone


class SubjectQuerySet(models.QuerySet):
    def last_subjects(self, number):
        return self.published_subjects()[:number]

    def published_subjects(self):
        return self.filter(timestamp__lte=timezone.now())

    def search(self, query):
        return self.filter((Q(title__icontains=query) | Q(content__icontains=query)).distinct())


class SubjectManager(models.Manager):
    def get_queryset(self):
        return SubjectQuerySet(self.model, using=self._db)

    def get_last_subjects(self, number):
        return self.get_queryset().last_subjects(number)

    def get_published_subjects(self):
        return self.get_queryset().published_subjects()

    def search(self, query):
        return self.get_queryset().search(query)
