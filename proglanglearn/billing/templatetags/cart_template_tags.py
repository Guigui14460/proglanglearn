from django import template

from billing.models import Order


register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs.first().courses.count()
    return 0


@register.filter
def zfill(number, fill):
    return str(number).zfill(int(fill))
