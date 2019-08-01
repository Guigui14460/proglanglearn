from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from accounts.models import Profile


def send_email_new_course(request, course):
    current_site = get_current_site(request)
    subject = _("Nouvelle formation en ligne")
    message = render_to_string('courses/new_course_email.html', {
        'protocol': settings.PROTOCOL,
        'domain': current_site.domain,
        'course': course
    })
    msg = EmailMultiAlternatives(
        subject, message, "ProgLangLearn", to=[profile.user.email for profile in Profile.objects.send_email()])
    msg.send()


mark_safe_lazy = lazy(mark_safe, str)
