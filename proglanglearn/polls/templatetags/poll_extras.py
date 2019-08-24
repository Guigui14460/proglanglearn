import datetime

from django import template
from django.template.loader import render_to_string
from django.utils.html import format_html

from polls.models import Poll, Item, Vote
from polls import views


register = template.Library()


@register.simple_tag(takes_context=True)
def poll(context):
    request = context['request']

    try:
        poll = Poll.published.latest("date")
    except Poll.DoesNotExists:
        return ''

    items = Item.objects.filter(poll=poll)

    if poll.get_cookie_name() in request.COOKIES:
        template = "polls/poll_result.html"
    else:
        template = "polls/poll_detail.html"

    content = render_to_string(template, {'poll': poll, 'items': items})
    return content


@register.simple_tag
def percentage(poll, item):
    if poll.votes > 0:
        return round(float(item.votes) / float(poll.votes) * 100, 2)
    return 0


@register.filter
def can_vote(poll, request):
    today = datetime.date.today()
    if poll.end_date is None:
        if not Vote.objects.filter(poll=poll, ip=request.META['REMOTE_ADDR']).exists():
            return False
    else:
        if not Vote.objects.filter(poll=poll, ip=request.META['REMOTE_ADDR']).exists() and poll.end_date < datetime.date.today():
            return False
    return True
