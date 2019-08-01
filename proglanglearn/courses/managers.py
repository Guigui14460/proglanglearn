from django.db import models
from django.db.models import Q
from django.utils import timezone


class CourseQuerySet(models.QuerySet):
    def last_courses(self, number):
        return self.published_courses()[number:]

    def published_courses(self):
        return self.filter(published=True, published_date__lte=timezone.now())

    def send_email(self):
        return self.filter(email_send=False, published=True, published_date__lte=timezone.now())

    def search(self, query):
        return self.filter((Q(title__icontains=query) | Q(content_introduction__icontains=query)).distinct())


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def get_last_courses(self, number):
        return self.get_queryset().last_courses(number)

    def get_published_courses(self):
        return self.get_queryset().published_courses()

    def get_send_email_course(self):
        return self.get_queryset().send_email()

    def search(self, query):
        return self.get_queryset().search(query)


class TutorialQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter((Q(title__icontains=query) | Q(content__icontains=query)).distinct())


class TutorialManager(models.Manager):
    def get_queryset(self):
        return TutorialQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)
