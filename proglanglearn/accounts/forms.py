from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm, PasswordChangeForm as BasePasswordChangeForm
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from form_utils.forms import BetterForm
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from main.models import Language
from .models import Profile


User = get_user_model()


PROG_TYPE = [
    ('A', _("Amateur")),
    ('E', _("Étudiant")),
    ('D', _("Développeur professionel"))
]


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
        if user.profile.strike >= settings.MAX_STRIKE:
            raise forms.ValidationError(
                _("Votre compte est banni. Vous n'y avez plus accès"))


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


class PasswordChangeForm(BasePasswordChangeForm):
    class Meta:
        widgets = {
            'old_password': forms.PasswordInput(attrs={
                'placeholder': '••••••••••',
                'id': 'showPWDInput'
            }),
            'new_password1': forms.PasswordInput(attrs={
                'placeholder': '••••••••••',
                'id': 'showNewPWDInput'
            }),
            'new_password2': forms.PasswordInput(attrs={
                'placeholder': '••••••••••',
                'id': 'showNewPWDConfirmInput'
            }),
        }


class ChangeProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'country']
        labels = {'image': _("Photo de profil")}
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'btn btn__block'}),
            'country': CountrySelectWidget(attrs={'style': 'width: 100%; font-size: 1.1rem;'})
        }
        help_text = {'country': _(
            "Le renseignement de votre pays permet aux étudiants de développeurs d'être mis en avant. Cette donnée est utilisée pour statistiques")}


class PersonalInformationForm(forms.Form):
    image = forms.ImageField(label=_("Photo de profil"), required=False,
                             widget=forms.ClearableFileInput(attrs={'class': 'btn btn__block'}))
    username = forms.CharField(label=_("Nom d'utilisateur"), widget=forms.TextInput(
        attrs={'placeholder': 'johndoe'}))
    email = forms.EmailField(label=_(
        "Addresse e-mail"), widget=forms.EmailInput(attrs={'placeholder': 'johndoe@gmail.com'}))
    first_name = forms.CharField(
        label=_("Prénom"), widget=forms.TextInput(attrs={'placeholder': 'John'}))
    last_name = forms.CharField(
        label=_("Nom"), widget=forms.TextInput(attrs={'placeholder': 'Doe'}))
    prog_type = forms.ChoiceField(label=_("Quel statut en programmation ou dans la vie avez-vous ?"), choices=PROG_TYPE, widget=forms.Select(attrs={'style': 'width: 100%; font-size: 1.1rem;'}), help_text=_(
        "Les statuts de développeur et étudiant permet de vous mettre en avant. En choisissant un de ces deux choix, vous activerez la visibilité totale de votre profil (informations éducatives et professionnelles"))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PersonalInformationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.count() > 0:
            if qs.first() != self.request.user:
                raise forms.ValidationError(
                    _("Cette addresse email a déjà été utilisée. Il faut en choisir une autre ou garder votre ancienne addresse si possible"))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.count() > 0:
            if qs.first() != self.request.user:
                raise forms.ValidationError(
                    _("Ce nom d'utilisateur a déjà été utilisée. Il faut en choisir un autre ou garder votre ancien nom d'utilisateur si possible"))
        return username


class ProfileInformationForm(forms.Form):
    biography = forms.CharField(max_length=1500, label=_("Biographie"), widget=forms.Textarea(attrs={'placeholder': _('Une courte biographie')}), required=False, help_text=_(
        "Courte biographie ou une phrase/expression que vous aimez pour vous décrire rapidement (1500 caractères)"))
    skills = forms.ModelMultipleChoiceField(label=_("Choisissez des compétences (langages ou framework"), queryset=Language.objects.all(), widget=forms.SelectMultiple, help_text=_(
        "N.B. : multiple sélection possible<br>S'il manque une bibliothèque ou un langage, demandez à le rajouter dans la page contact."))
    website_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre site web')}))
    twitter_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profile Twitter')}))
    youtube_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre chaîne Youtube')}))
    facebook_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profile Facebook')}))
    linked_in_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profile LinkedIn')}))
    instagram_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profile Intagram')}))
    github = forms.CharField(required=False, label=_("Email ou nom d'utilisateur de votre compte Github"), widget=forms.TextInput(attrs={'placeholder': 'johndoe93'}), help_text=_(
        "<i class='fas fa-exclamation-triangle'></i> En renseignant ce champ, vous accepter de publier les liens et les informations de vos dépôts publics de votre compte Github"))


class DangerZoneForm(forms.Form):
    error_messages = {
        'password_incorrect': _("Le mot de passe que vous avez entrez est incorrect. Veuillez réessayer."),
    }

    password = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••••',
        'id': 'showPWDDeleteConfirmInput'
    }))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(DangerZoneForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return password


class DeleteAccountForm(forms.Form):
    confirm = forms.CharField(min_length=len(_("CONFIRMER")), max_length=len(_("CONFIRMER")), label=_("Confirmer"), widget=forms.TextInput(
        attrs={'placeholder': _("CONFIRMER")}), help_text=_("Écrire 'CONFIRMER' en majuscule pour confirmer la suppression"))

    def clean_confirm(self):
        confirm = self.cleaned_data.get('confirm')
        if confirm == _("CONFIRMER"):
            raise forms.ValidationError(
                _("Écrivez 'CONFIRMER' dans la langue actuelle du site"))
        return confirm
