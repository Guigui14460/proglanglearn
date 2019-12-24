from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _

from .models import Profile


User = get_user_model()


class ProfileObjectMixin(object):
    model = Profile

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        obj = None
        if id is not None:
            obj = get_object_or_404(User, id=user_id)
        return obj.profile


class UserCanModifyProfile(UserPassesTestMixin):
    permission_denied_message = _(
        "Vous n'avez pas l'autorisation de modifier ce profil")

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            obj = self.get_object()
            if obj is not None:
                messages.error(self.request, self.permission_denied_message)
                return redirect('accounts:profile', user_id=obj.user.id)
            messages.info(self.request, _(
                "Le profil auquel vous essayez d'accéder n'existe pas, ou plus, ou est actuellement inaccessible"))
            return Http404
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return user == obj.user
