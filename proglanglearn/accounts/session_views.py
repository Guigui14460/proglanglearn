from django.shortcuts import render
from django.urls import reverse_lazy

from user_sessions.views import (
    SessionDeleteOtherView as BaseSessionDeleteOtherView,
    SessionDeleteView as BaseSessionDeleteView,
    SessionListView as BaseSessionListView
)

from main.mixins import NavbarSearchMixin


class SessionDeleteOtherView(NavbarSearchMixin, BaseSessionDeleteOtherView):
    def get_success_url(self):
        return str(reverse_lazy('accounts:session_list'))


class SessionDeleteView(NavbarSearchMixin, BaseSessionDeleteView):
    def get_success_url(self):
        return str(reverse_lazy('accounts:session_list'))


class SessionListView(NavbarSearchMixin, BaseSessionListView):
    pass
