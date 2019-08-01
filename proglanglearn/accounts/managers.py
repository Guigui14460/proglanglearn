from django.db import models


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
