from django import template


register = template.Library()


@register.filter('id_for_view_password')
def id_for_view_password(id):
    return id.replace('Input', '')
