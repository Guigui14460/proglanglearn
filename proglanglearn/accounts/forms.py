from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField


User = get_user_model()


class SignUpForm(UserCreationForm):
    username = forms.CharField(label=_("Nom d'utilisateur"), widget=forms.TextInput(attrs={
        'placeholder': 'johndoe',
        'autofocus': 'autofocus'
    }))
    email = forms.EmailField(label=_("Courriel"), widget=forms.TextInput(attrs={
        'placeholder': 'johndoe@example.com',
        'type': 'email',
        'name': 'email'
    }), help_text=_("Informez une addresse e-mail valide"), required=True)
    password1 = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••••',
        'id': 'showPWDInput'
    }), help_text=_("""Entrez un mot de passe fort (avec minuscule, majuscule, chiffres et caractères spéciaux)
    Votre mot de passe ne devrait pas contenir ou ressembler à votre nom d'utilisateur.
    Il doit aussi contenir %(password_length)d caractères.""") % {'password_length': 12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length']})
    password2 = forms.CharField(label=_("Confirmation du mot de passe"), widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••••',
        'id': 'showPWDConfirmInput'
    }), help_text=_("Entrez le même mot de passe"))
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                _("Cette addresse email a déjà été utilisée. Il faut en choisir une autre"))
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Nom d'utilisateur"), widget=forms.TextInput(attrs={
        'placeholder': 'johndoe',
        'autofocus': 'autofocus'
    }))
    password = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••••',
        'id': 'showPWDInput'
    }))
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username) == []:
            raise forms.ValidationError(
                _("Le nom d'utilisateur mentionné n'existe pas"))
        return username

    def confirm_login_allowed(self, user):
        if not user.profile.email_confirmed:
            messages.error(self.request, _(
                "Votre compte n'a pas été activé. Vérifiez vos emails et votre dossier spam et si vous ne trouvez pas le mail, réinscrivez-vous avec les identifiants renseignés"))
            raise forms.ValidationError('')


class PasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'off', 'id': 'showPWDInput'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'off', 'id': 'showPWDConfirmInput'}),
    )
    captcha = ReCaptchaField()
