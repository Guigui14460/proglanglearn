from django.conf import settings
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
        if settings.SEARCH_TYPE == 'multiple':
            return self.search_multiple(query)
        elif settings.SEARCH_TYPE == 'simple':
            return self.search_simple(query)
        return self.none()

    def search_simple(self, query):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | Q(
                content_introduction__icontains=query))
            qs = qs.filter(or_lookup).filter(
                published=True, published_date__lte=timezone.now())
        return qs

    def search_multiple(self, query):
        qs = self.none()
        if query is not None:
            for word in query.split():
                or_lookup = (Q(title__icontains=word) | Q(
                    content_introduction__icontains=word))
                qs = qs | self.get_queryset().filter(or_lookup).filter(
                    published=True, published_date__lte=timezone.now())
            qs.distinct()
        return qs


class TutorialQuerySet(models.QuerySet):
    pass


class TutorialManager(models.Manager):
    def get_queryset(self):
        return TutorialQuerySet(self.model, using=self._db)

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
            qs = qs.filter(or_lookup).filter(
                published_date__lte=timezone.now())
        return qs

    def search_multiple(self, query):
        qs = self.none()
        if query is not None:
            for word in query.split():
                or_lookup = (Q(title__icontains=word) |
                             Q(content__icontains=word))
                qs = qs | self.get_queryset().filter(or_lookup).filter(
                    published_date__lte=timezone.now())
            qs.distinct()
        return qs
