from django.core.mail import send_mail

from allauth.account.views import (
    LoginView as AllauthLoginView,
    LogoutView as AllauthLogoutView,
    SignupView as AllauthSignupView,
    PasswordChangeView as AllauthPasswordChangeView,
    PasswordSetView as AllauthPasswordSetView,
    PasswordResetView as AllauthPasswordResetView,
    PasswordResetDoneView as AllauthPasswordResetDoneView,
    PasswordResetFromKeyView as AllauthPasswordResetFromKeyView,
    PasswordResetFromKeyDoneView as AllauthPasswordResetFromKeyDoneView,
    EmailView as AllauthEmailView,
    ConfirmEmailView as AllauthConfirmEmailView,
    AccountInactiveView as AllauthAccountInactiveView,
    EmailVerificationSentView as AllauthEmailVerificationSentView,
)

from main.mixins import NavbarSearchMixin
from main.utils import get_ip_address_client


class LoginView(NavbarSearchMixin, AllauthLoginView):
    def post(self, *args, **kwargs):
        older_post = super(LoginView, self).post(*args, **kwargs)
        ip_address = get_ip_address_client(self.request)
        print(ip_address)
        if self.request.user.ip_address == None:
            self.request.user.ip_address = ip_address
            self.request.user.save()
        else:
            if ip_address != self.request.user.ip_address:
                send_mail("Votre compte a sûrement été compromis",
                          "<ip_addess_of_atk>")
        return older_post


class LogoutView(NavbarSearchMixin, AllauthLogoutView):
    pass


class SignupView(NavbarSearchMixin, AllauthSignupView):
    def post(self, *args, **kwargs):
        older_post = super(SignupView, self).post(*args, **kwargs)
        self.request.user.ip_address = get_ip_address_client(self.request)
        self.request.user.save()
        return older_post


class PasswordChangeView(NavbarSearchMixin, AllauthPasswordChangeView):
    pass


class PasswordSetView(NavbarSearchMixin, AllauthPasswordSetView):
    pass


class PasswordResetView(NavbarSearchMixin, AllauthPasswordResetView):
    pass


class PasswordResetDoneView(NavbarSearchMixin, AllauthPasswordResetDoneView):
    pass


class PasswordResetFromKeyView(NavbarSearchMixin, AllauthPasswordResetFromKeyView):
    pass


class PasswordResetFromKeyDoneView(NavbarSearchMixin, AllauthPasswordResetFromKeyDoneView):
    pass


class EmailView(NavbarSearchMixin, AllauthEmailView):
    pass


class ConfirmEmailView(NavbarSearchMixin, AllauthConfirmEmailView):
    pass


class AccountInactiveView(NavbarSearchMixin, AllauthAccountInactiveView):
    pass


class EmailVerificationSentView(NavbarSearchMixin, AllauthEmailVerificationSentView):
    pass
