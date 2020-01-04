from django.conf import settings
from django.db import models
from django.db.models import Q


class ProfileQuerySet(models.QuerySet):
    def dev_profile_shown(self):
        return self.filter(is_dev=True, public_profile=True)

    def student_profile_shown(self):
        return self.filter(is_student=True, public_profile=True)

    def email(self):
        return self.filter(user__is_active=True)

    def all_profile(self):
        return self.filter(public_profile=True)


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def full_profile_shown(self):
        return self.get_queryset().all_profile().order_by('-public_profile', '-is_dev', '-is_student')

    def send_email(self):
        return self.get_queryset().email()

    def all_dev_student(self):
        return self.get_queryset().filter((Q(public_profile=True) & (Q(is_dev=True) | Q(is_student=True))))

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
            qs = qs.filter((or_lookup & Q(public_profile=True)
                            & (Q(is_dev=True) | Q(is_student=True))))
        return qs

    def search_multiple(self, query):
        qs = self.none()
        if query is not None:
            for word in query.split():
                or_lookup = (Q(user__username__icontains=word) | Q(
                    user__first_name__icontains=word) | Q(user__last_name__icontains=word))
                qs = qs | self.get_queryset().filter(
                    (or_lookup & Q(public_profile=True) & (Q(is_dev=True) | Q(is_student=True))))
            qs.distinct()
        return qs
