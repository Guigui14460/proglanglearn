from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _

import os
import pandas as pd


df = pd.read_csv(os.path.join(settings.BASE_DIR,
                              'accounts/datasets/levels.csv'))


def get_last_level(df):
    level_column = df['level']
    return level_column.iloc[-1]


def get_exp_limit(df, level):
    exp_column = df['experience']
    try:
        return exp_column[level + 1]
    except:
        return exp_column.iloc[-1]


MAX_LEVEL = get_last_level(df)
MAX_EXPERIENCE = get_exp_limit(df, 100)


def check_level(request, actual_user_level=None, user_experience=None):
    if actual_user_level is None:
        actual_user_level = request.user.profile.level
    if user_experience is None:
        user_experience = request.user.profile.level_experience
    next_experience_limit = get_exp_limit(df, actual_user_level)
    if user_experience > next_experience_limit:
        if user_experience > MAX_EXPERIENCE and actual_user_level == MAX_LEVEL:
            return actual_user_level
        actual_user_level += 1
        next_experience_limit = get_exp_limit(df, actual_user_level)
        if actual_user_level == get_last_level(df):
            messages.success(request, _(
                "Vous êtes déjà au niveau maximum ! Continuez de vous formez et d'apprendre car de nouveaux niveaux seront rajoutés ;)"))
        else:
            messages.info(request, _(
                f"Bravo ! Vous venez de gagner un niveau ! Vous êtes désormais niveau {actual_user_level}"))
        return check_level(request, actual_user_level=actual_user_level, user_experience=user_experience)

    request.user.profile.level = actual_user_level
    request.user.profile.save()
    return actual_user_level


def get_user_type(user):
    return None
