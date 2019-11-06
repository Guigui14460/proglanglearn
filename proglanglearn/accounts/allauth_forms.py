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
            }))
        self.fields['password2'] = forms.CharField(
            min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
                1]['OPTIONS']['min_length'],
            label=_("Confirmation du mot de passe"),
            widget=forms.PasswordInput(attrs={
                'placeholder': '••••••••••',
                'id': 'showConfirmPWDInput'
            }))
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
        }))
    password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Confirmation du nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showConfirmNewPWDInput'
        }))
    captcha = ReCaptchaField()


class SetPasswordForm(AllauthSetPasswordForm):
    password1 = SetPasswordField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showPWDInput'
        }))
    password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Confirmation du mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showConfirmPWDInput'
        }))
    captcha = ReCaptchaField()


class ResetPasswordKeyForm(AllauthResetPasswordKeyForm):
    password1 = SetPasswordField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showNewPWDInput'
        }))
    password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Confirmation du nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showConfirmNewPWDInput'
        }))
    captcha = ReCaptchaField()
