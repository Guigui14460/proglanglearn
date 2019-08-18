from django.conf import settings
from django.db import models
from django.db.models import Q


class ProfileQuerySet(models.QuerySet):
    def dev_profile_shown(self):
        return self.filter(is_dev=True)

    def student_profile_shown(self):
        return self.filter(is_student=True)

    def email(self):
        return self.filter(email_notification=True)


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def full_profile_shown(self):
        return (self.get_queryset().dev_profile_shown() | self.get_queryset().student_profile_shown()).distinct()

    def send_email(self):
        return self.get_queryset().email()

    def search(self, query):
        if settings.SEARCH_TYPE == 'multiple':
            return self.search_multiple(query)
        elif settings.SEARCH_TYPE == 'simple':
            return self.search_simple(query)
        return self.none()

    def search_simple(self, query):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(user__username__icontains=query) | Q(
                user__first_name__icontains=query) | Q(user__last_name__icontains=query))
            qs = qs.filter(or_lookup)
        return qs

    def search_multiple(self, query):
        qs = self.none()
        if query is not None:
            for word in query.split():
                or_lookup = (Q(user__username__icontains=word) | Q(
                    user__first_name__icontains=word) | Q(user__last_name__icontains=word))
                qs = qs | self.get_queryset().filter(or_lookup)
            qs.distinct()
        return qs
