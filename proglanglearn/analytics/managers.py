from django.db import models


class UserExperienceJournalQuerySet(models.QuerySet):
    def last_journals(self, user, number):
        return self.user_journals(user)[:number]

    def user_journals(self, user):
        return self.filter(user=user)


class UserExperienceJournalManager(models.Manager):
    def get_queryset(self):
        return UserExperienceJournalQuerySet(self.model, using=self._db)

    def get_last_journals(self, user, number):
        return self.get_queryset().last_journals(user, number)
