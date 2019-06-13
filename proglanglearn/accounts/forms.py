from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Mot de passe"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Confirmation du mot de passe"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Vos mot de passe sont différents"))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    query = forms.CharField(label=_("Nom d'utilisateur / E-mail"))
    password = forms.CharField(
        label=_("Mot de passe"), widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) | Q(email_iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError(
                _("Justificatifs invalides. L'utilisateur n'existe pas"))
        user_obj = user_qs_final.first()
        if not user_obj.is_active:
            raise forms.ValidationError(
                _("Le compte a été fermé par le titulaire ou a été banni"))
        if not user_obj.check_password(password):
            raise forms.ValidationError(_("Champs renseignés incorrects"))
        self.cleaned_data['user_obj'] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)
