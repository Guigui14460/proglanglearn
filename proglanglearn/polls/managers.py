from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(is_published=True, end_date__lte=timezone.now())
