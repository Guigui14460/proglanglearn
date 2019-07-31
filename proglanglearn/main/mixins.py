from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

from .forms import NavbarSearchForm
from .signals import comment_signal


class NavbarSearchMixin(object):
    model = None

    def form_navbar(self):
        form = NavbarSearchForm()
        if form.is_valid():
            form = NavbarSearchForm(q=form.cleaned_data.get('q'))
        return form


class IsStaff(UserPassesTestMixin):
    permission_denied_message = _(
        "La page auquel vous essayez d'accéder n'est accessible que par les administrateurs du site")

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return user.is_staff
        return False

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return HttpResponseForbidden
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
