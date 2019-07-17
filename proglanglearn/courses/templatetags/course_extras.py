from django import template


register = template.Library()


@register.filter('time_estimate')
def time_estimate(words):
    word_count = len(words.split())
    return round(word_count / 50)
