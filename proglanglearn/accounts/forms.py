from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.db.models import Q
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
    }), help_text=_(""))
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
            raise ValidationError(
                _("Cette addresse email a déjà été utilisée. Il faut en choisir une autre"))
        return email

    def save(self):
        user = super(SignUpForm, self).save(commit=False)
        user.is_active = False
        user.save()
        return user


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
            raise forms.ValidationError(_("Le nom d'utilisateur mentionné n'existe pas"))
        return username
    
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.profile.email_confirmed:
            raise forms.ValidationError(_("Votre compte n'a pas été activé. Vérifiez vos emails et votre dossier spam et si vous ne trouvez pas le mail, réinscrivez-vous avec les identifiants renseignés"))

class PasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'id': 'showPWDInput'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'id': 'showPWDConfirmInput'}),
    )
    captcha = ReCaptchaField()
