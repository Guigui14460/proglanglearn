from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.utils.translation import ngettext
from django.views.generic import TemplateView

from main.mixins import NavbarSearchMixin
from .utils import get_recent_user_exp_journal


class DashboardView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'dashboard'
        context['activate'] = 'dashboard'
        context['label'], context['data'] = get_recent_user_exp_journal(
            self.request.user)
        context['strike'] = ngettext(
            'Vous avez %(count)d signalement. Cliquez <a href="%(url)s" title="Les signalements">ici</a> pour en savoir plus',
            'Vous avez %(count)d signalements. Cliquez <a href="%(url)s" title="Les signalements">ici</a> pour en savoir plus',
            self.request.user.profile.strike) % {'count': self.request.user.profile.strike, 'url': reverse('main:terms')}
        return context
