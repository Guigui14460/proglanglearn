import datetime

from django import template
from django.contrib.auth import get_user_model


User = get_user_model()

register = template.Library()


@register.filter
def class_name(value):
    return value.__class__.__name__


@register.simple_tag(takes_context=True)
def current_year(context):
    request = context.get('request')
    return datetime.date.today().year


@register.simple_tag(takes_context=True)
def admin_url(context):
    request = context.get('request')
    return User.objects.get(email='proglanglearn@gmail.com', is_superuser=True).profile.get_absolute_url()
