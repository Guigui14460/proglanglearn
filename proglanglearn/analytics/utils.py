from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime, now, timedelta
from django.utils.translation import gettext_lazy as _
import pytz

from accounts.utils import check_level
from .models import UserExperienceJournal


MONTHS = [_('Janvier'), _('Février'), _('Mars'),
          _('Avril'), _('Mai'), _('Juin'),
          _('Juillet'), _('Août'), _('Septembre'),
          _('Octobre'), _('Novembre'), _('Décembre')
          ]


def save_user_exp(request, exp):
    today = now()
    try:
        obj = UserExperienceJournal.objects.get(user=request.user, timestamp__gte=datetime(
            today.year, today.month, today.day, 0, 0, 0, 0, tzinfo=pytz.UTC), timestamp__lt=datetime(today.year, today.month, today.day + 1, 0, 0, 0, 0, tzinfo=pytz.UTC))
    except UserExperienceJournal.DoesNotExist:
        obj = UserExperienceJournal.objects.create(
            user=request.user,
            experience=exp,
        )
    check_level(request)


def get_recent_user_exp_journal(user):
    today = now()
    x_list, y_list = [], []
    for i in reversed(range(7)):
        try:
            to_append = UserExperienceJournal.objects.get(
                user=user,
                timestamp__gte=datetime(
                    today.year, today.month, today.day, 0, 0, 0, 0, tzinfo=pytz.UTC) - timedelta(days=i),
                timestamp__lt=datetime(
                    today.year, today.month, today.day + 1, 0, 0, 0, 0, tzinfo=pytz.UTC) - timedelta(days=i)
            )
            x = datetime(today.year, today.month, today.day, 0, 0,
                         0, 0, tzinfo=pytz.UTC) - timedelta(days=i)
            y = to_append.experience
        except:
            x = datetime(today.year, today.month, today.day, 0, 0,
                         0, 0, tzinfo=pytz.UTC) - timedelta(days=i)
            y = 0
        str_x = f"{x.day} {MONTHS[x.month - 1]} {x.year}"
        x_list.append(str_x)
        y_list.append(y)
    return x_list, y_list
