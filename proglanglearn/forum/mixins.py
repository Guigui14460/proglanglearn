from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _

from .models import Subject


class SubjectObjectMixin(object):
    model = Subject

    def get_object(self):
        id = self.kwargs.get('id')
        if id is None:
            id = self.kwargs.get('subject_id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class UserCanModifySubject(UserPassesTestMixin):
    permission_denied_message = _(
        "Vous n'avez pas l'autorisation de modifier ce sujet")

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            subject = self.get_object()
            if subject is not None:
                messages.error(self.request, self.permission_denied_message)
                return redirect('subjects:list')
            messages.info(self.request, _(
                "Le sujet auquel vous essayez d'accéder n'existe pas ou plus ou est actuellement inaccessible"))
            return Http404
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def test_func(self):
        user = self.request.user
        subject = self.get_object()
        return user.is_staff or subject.user == user
