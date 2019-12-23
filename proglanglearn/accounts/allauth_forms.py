from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import (
    SetPasswordField,
    LoginForm as AllauthLoginForm,
    SignupForm as AllauthSignupForm,
    ChangePasswordForm as AllauthChangePasswordForm,
    SetPasswordForm as AllauthSetPasswordForm,
    ResetPasswordKeyForm as AllauthResetPasswordKeyForm,
)
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class LoginForm(AllauthLoginForm):
    password = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showPWDInput'
        }))
    captcha = ReCaptchaField()


class SignupForm(AllauthSignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = forms.CharField(
            min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
                1]['OPTIONS']['min_length'],
            label=_("Mot de passe"),
            widget=forms.PasswordInput(attrs={
                'placeholder': '••••••••••',
                'id': 'showPWDInput'
            }), help_text=_("""Entrez un mot de passe fort (avec minuscule, majuscule, chiffres et caractères spéciaux).<br>Votre mot de passe ne devrait pas contenir ou ressembler à votre nom d'utilisateur.<br>Il doit contenir au minimum %(password_length)d caractères.""") % {'password_length': 12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length']})
        self.fields['password2'] = forms.CharField(
            min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
                1]['OPTIONS']['min_length'],
            label=_("Confirmation du mot de passe"),
            widget=forms.PasswordInput(attrs={
                'placeholder': '••••••••••',
                'id': 'showConfirmPWDInput'
            }), help_text=_("Entrez le même mot de passe"))
        captcha = ReCaptchaField()


class ChangePasswordForm(AllauthChangePasswordForm):
    oldpassword = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Mot de passe actuel"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showOldPWDInput'
        }))
    password1 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showNewPWDInput'
        }), help_text=_("""Entrez un mot de passe fort (avec minuscule, majuscule, chiffres et caractères spéciaux).<br>Votre mot de passe ne devrait pas contenir ou ressembler à votre nom d'utilisateur.<br>Il doit contenir au minimum %(password_length)d caractères.""") % {'password_length': 12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length']})
    password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Confirmation du nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showConfirmNewPWDInput'
        }), help_text=_("Entrez le même mot de passe"))
    captcha = ReCaptchaField()


class SetPasswordForm(AllauthSetPasswordForm):
    password1 = SetPasswordField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showPWDInput'
        }), help_text=_("""Entrez un mot de passe fort (avec minuscule, majuscule, chiffres et caractères spéciaux).<br>Votre mot de passe ne devrait pas contenir ou ressembler à votre nom d'utilisateur.<br>Il doit contenir au minimum %(password_length)d caractères.""") % {'password_length': 12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length']})
    password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Confirmation du mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showConfirmPWDInput'
        }), help_text=_("Entrez le même mot de passe"))
    captcha = ReCaptchaField()


class ResetPasswordKeyForm(AllauthResetPasswordKeyForm):
    password1 = SetPasswordField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showNewPWDInput'
        }), help_text=_("""Entrez un mot de passe fort (avec minuscule, majuscule, chiffres et caractères spéciaux).<br>Votre mot de passe ne devrait pas contenir ou ressembler à votre nom d'utilisateur.<br>Il doit contenir au minimum %(password_length)d caractères.""") % {'password_length': 12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length']})
    password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Confirmation du nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showConfirmNewPWDInput'
        }), help_text=_("Entrez le même mot de passe"))
    captcha = ReCaptchaField()
