from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

from .forms import NavbarSearchForm
from .signals import comment_signal
from .thread_remove_useless_info import DeleteUselessData


class NavbarSearchMixin(object):
    model = None

    def form_navbar(self):
        nav_form = NavbarSearchForm()
        return nav_form

    def get_context_data(self, **kwargs):
        thread = DeleteUselessData()
        thread.start()
        try:
            context = super().get_context_data(**kwargs)
        except AttributeError:
            context = {**kwargs}
        context['navbar_search_form'] = self.form_navbar()
        context['last_privacy'] = settings.LAST_PRIVACY
        return context


class IsStaff(UserPassesTestMixin):
    permission_denied_message = _(
        "La page que vous essayez d'accéder n'est accessible que par les administrateurs du site")

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
