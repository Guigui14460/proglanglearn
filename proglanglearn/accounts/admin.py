from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Profile

admin.site.unregister(Group)
admin.site.register(Profile)
