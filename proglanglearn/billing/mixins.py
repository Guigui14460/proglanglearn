from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from .models import Order


class UserCanViewCheckout(UserPassesTestMixin):
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(self.request, _(
                "Vous ne pouvez pas accéder à la page de paiement. Il vous impérativement mettre un cours dans votre panier"))
            return redirect('courses:list')
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def test_func(self):
        user = self.request.user
        order_qs = Order.objects.filter(user=user, ordered=False)
        return order_qs.exists() and order_qs.first().courses.all().count() > 0
