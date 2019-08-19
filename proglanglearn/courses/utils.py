from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import activate, get_language, gettext as _

from accounts.models import Profile


def send_email_new_course(request, course):
    actual = get_language()
    all_profile = Profile.objects.send_email()
    french_profile, english_profile = [profile.user.email for profile in all_profile if profile.user.natural_language == 'fr'], [
        profile.user.email for profile in all_profile if profile.user.natural_language == 'en']
    current_site = get_current_site(request)
    protocol = settings.PROTOCOL
    domain = current_site.domain

    activate('fr')
    subject1 = _("Nouvelle formation en ligne")
    message1 = render_to_string('courses/new_course_email.html', {
        'protocol': protocol,
        'domain': domain,
        'course': course
    })

    activate('en')
    subject2 = _("Nouvelle formation en ligne")
    message2 = render_to_string('courses/new_course_email.html', {
        'protocol': protocol,
        'domain': domain,
        'course': course
    })

    datatuple = (
        (subject1, message1, settings.DEFAULT_FROM_EMAIL, french_profile),
        (subject2, message2, settings.DEFAULT_FROM_EMAIL, english_profile),
    )
    send_mass_mail(datatuple, fail_silently=True)

    activate(actual)


mark_safe_lazy = lazy(mark_safe, str)
