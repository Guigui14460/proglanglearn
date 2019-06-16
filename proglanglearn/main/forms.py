from django import forms
from django.utils.translation import gettext_lazy as _


class NavbarSearchForm(forms.Form):
    q = forms.CharField(label=_("Recherche"), widget=forms.TextInput(attrs={
        'id': 'search',
        'placeholder': _("Recherche"),
        'name': 'q'
    }), required=False)