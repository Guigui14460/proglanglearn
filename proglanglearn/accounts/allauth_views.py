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


class LoginView(NavbarSearchMixin, AllauthLoginView):
    pass


class LogoutView(NavbarSearchMixin, AllauthLogoutView):
    pass


class SignupView(NavbarSearchMixin, AllauthSignupView):
    pass


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