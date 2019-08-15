from django import template
from django.utils.translation import gettext as _

from courses.utils import mark_safe_lazy


register = template.Library()


@register.filter('time_estimate')
def time_estimate(words):
    word_count = len(words.split())
    return round(word_count / 50)


@register.filter
def safe_lazy(text):
    return mark_safe_lazy(_(text))


@register.filter
def index(liste, i):
    return liste[int(i)]
