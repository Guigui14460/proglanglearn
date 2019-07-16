from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

import random
import string


def random_string_generator(size=15, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, random=True, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        if random:
            slug = random_string_generator()
        else:
            slug = slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug)
    if qs.exists():
        new_slug = f"{slug}-{random_string_generator()}"
        return unique_slug_generator(instance, random=random, new_slug=new_slug)
    return slug


def get_ip_address_client(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOVE_ADDR', None)
    return ip


def get_thumbnail_preview(obj):
    if obj.pk:
        return mark_safe("""<a href="{src}" target="_blank"><img src="{src}" alt="{title}" style="width: 100%; height: auto;" /></a>""".format(
            src=obj.thumbnail.url,
            title=obj.title,
        ))
    return _("Choisissez une image et continuez d'éditer pour voir la prévisualisation de l'image")


get_thumbnail_preview.allow_tags = True
get_thumbnail_preview.short_description = _("Visualisation de la vignette")
