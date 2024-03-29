from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm, PasswordChangeForm as BasePasswordChangeForm
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from tinymce.widgets import TinyMCE

from main.models import Language
from .models import ProgType, Profile, Education, Experience


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
    password1 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••',
            'id': 'showPWDInput'
        }), help_text=_("""Entrez un mot de passe fort (avec minuscules, majuscules, chiffres et caractères spéciaux).<br>Votre mot de passe ne devrait pas contenir ou ressembler à votre nom d'utilisateur.<br>Il doit contenir au minimum %(password_length)d caractères.""") % {'password_length': 12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length']})
    password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Confirmation du mot de passe"),
        widget=forms.PasswordInput(attrs={
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
    password = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
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
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'off', 'id': 'showPWDInput'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[
            1]['OPTIONS']['min_length'],
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'off', 'id': 'showPWDConfirmInput'}),
    )
    captcha = ReCaptchaField()


class PasswordChangeForm(BasePasswordChangeForm):
    old_password = forms.CharField(min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length'], label=_("Ancien mot de passe"), widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••••',
        'id': 'showPWDInput'
    }), help_text=_("Entrez votre mot de passe actuel"))
    new_password1 = forms.CharField(min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length'], label=_("Nouveau mot de passe"), widget=forms.PasswordInput(attrs={
        'id': 'showNewPWDInput', 'placeholder': '••••••••••'
    }), help_text=_("""Entrez un mot de passe fort (avec minuscules, majuscules, chiffres et caractères spéciaux).<br>Votre mot de passe ne devrait pas contenir ou ressembler à votre nom d'utilisateur.<br>Il doit contenir au minimum %(password_length)d caractères.""") % {'password_length': 12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length']})
    new_password2 = forms.CharField(min_length=12 if settings.DEBUG else settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length'], label=_("Confirmation du nouveau mot de passe"), widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••••',
        'id': 'showNewPWDConfirmInput'
    }), help_text=_("Entrez le même mot de passe"))
    captcha = ReCaptchaField()


class ChangeProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        labels = {'image': _("Photo de profil")}
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'btn btn__block'}),
        }


class PersonalInformationForm(forms.Form):
    username = forms.CharField(label=_("Nom d'utilisateur"), widget=forms.TextInput(
        attrs={'placeholder': 'johndoe', 'id': 'username_id_custom'}))
    first_name = forms.CharField(
        label=_("Prénom"), widget=forms.TextInput(attrs={'placeholder': 'John'}))
    last_name = forms.CharField(
        label=_("Nom"), widget=forms.TextInput(attrs={'placeholder': 'Doe'}))
    email_notification = forms.BooleanField(required=False, label=_(
        "Recevoir des notifications par email"), widget=forms.CheckboxInput)
    public_profile = forms.BooleanField(required=False, label=_(
        "Rendre mon profil public"), widget=forms.CheckboxInput, help_text=_("Votre profil sera visible mais pas indexé lors de la recherche de profils"))
    prog_type = forms.ModelChoiceField(label=_("Quel statut en programmation ou dans la vie avez-vous ?"), queryset=ProgType.objects.all(), widget=forms.Select(attrs={'style': 'width: 100%; font-size: 1.1rem;'}), help_text=_(
        "Les statuts de développeur et étudiant permet de vous mettre en avant. Cela vous permet de vous indexé lors des recherches de profils."))
    country = CountryField(blank_label=_("Sélectionner un pays")).formfield(widget=CountrySelectWidget(attrs={'style': 'width: 100%; font-size: 1.1rem;'}), label=_(
        "Pays"), help_text=_("Le renseignement de votre pays permet aux étudiants et développeurs d'être mis en avant. Cette donnée est utilisée pour des études statistiques."))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PersonalInformationForm, self).__init__(*args, **kwargs)
        if len(self.request.user.socialaccount_set.all()) > 0:
            social_account = self.request.user.socialaccount_set.all()[0]
            if social_account.provider in ["google", "twitter"]:
                del self.fields['last_name']
                del self.fields['first_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.count() > 0:
            if qs.first() != self.request.user:
                raise forms.ValidationError(
                    _("Cette adresse email a déjà été utilisée. Il faut en choisir une autre ou garder votre ancienne adresse si possible"))
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
        "Courte biographie ou une phrase/expression que vous aimez pour vous décrire rapidement (1500 caractères)."))
    skills = forms.ModelMultipleChoiceField(required=False, label=_("Choisissez des compétences (langages ou frameworks)"), queryset=Language.objects.all(), widget=forms.SelectMultiple(attrs={
        'class': 'custom-multiple-select select-multiple__light', 'size': 7,
    }), help_text=_(
        "N.B. : multiple sélection possible.<br>S'il manque une bibliothèque ou un langage, demandez à le rajouter dans la page contact."))
    website_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre site web')}))
    twitter_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profil Twitter')}))
    youtube_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre chaîne Youtube')}))
    facebook_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profil Facebook')}))
    linked_in_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profil LinkedIn')}))
    instagram_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': _('URL de votre profil Instagram')}))
    github = forms.CharField(required=False, label=_("Nom d'utilisateur de votre compte Github"), widget=forms.TextInput(attrs={'placeholder': 'johndoe93'}), help_text=_(
        "<i class='fas fa-exclamation-triangle'></i> En renseignant ce champ, vous accepter de publier les liens et les informations de vos dépôts publics de votre compte Github."))


class DangerZoneForm(forms.Form):
    error_messages = {
        'password_incorrect': _("Le mot de passe que vous avez entré est incorrect. Veuillez réessayer."),
    }

    password = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••••',
        'id': 'showPWDDeleteConfirmInput',
    }))
    hidden = forms.HiddenInput()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(DangerZoneForm, self).__init__(*args, **kwargs)
        if len(self.user.socialaccount_set.all()) > 0:
            del self.fields['password']

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return password


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'description2',
                  'entry_date', 'exit_date']
        widgets = {
            'school': forms.TextInput(attrs={'placeholder': 'Epitech'}),
            'degree': forms.TextInput(attrs={'placeholder': _('Master en sécurité informatique')}),
            'description2': TinyMCE(attrs={'placeholder': _("Renseignements ..."), 'rows': 5}),
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
            'exit_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_text = {
            'description2': _("Vous pouvez donner quelques renseignements sur les compétences acquises, vos résultats, etc")
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['entreprise', 'employment',
                  'description', 'entry_date', 'exit_date']
        widgets = {
            'entreprise': forms.TextInput(attrs={'placeholder': 'Google'}),
            'employment': forms.TextInput(attrs={'placeholder': _("Analyste de données")}),
            'description': forms.Textarea(attrs={'placeholder': _("Renseignements ...")}),
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
            'exit_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_text = {
            'description': _("Vous pouvez donner quelques renseignements sur le type d'emploi où vous êtes/étiez affecté, les compétences demandées/requises, ce que vous faîtes/faisiez, etc")
        }


class ProfileSearchForm(forms.Form):
    q_profile = forms.CharField(label=_("Recherche de profil"), widget=forms.TextInput(attrs={
        'id': 'profile_search',
        'placeholder': _("Nom d'utilisateur, prénom ou nom de famille")
    }), required=False, help_text=_("N.B. : séparez les mots clés par des espaces pour plus de résultats."))
