from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment, CommentReport


QUERY_SEARCH_TYPE = (
    ('A', _("Tout")),
    ('B', _("Seulement les cours")),
    ('C', _("Seulement les tutoriels")),
    ('D', _("Seulement les articles")),
    ('E', _("Seulement les sujets")),
    ('F', _("Seulement les langages, bibliothèques et catégories")),
)


class NavbarSearchForm(forms.Form):
    q = forms.CharField(label=_("Recherche"), widget=forms.TextInput(attrs={
        'id': 'search',
        'placeholder': _("Recherche"),
        'name': 'q'
    }), required=False)


class SearchForm(forms.Form):
    q2 = forms.CharField(label=_("Recherche"), widget=forms.TextInput(attrs={
        'id': 'main_search',
        'placeholder': _("Recherche"),
        'name': 'q'
    }), required=False, help_text=_("N.B. : séparez les mots clés par des espaces pour plus de résultats"))
    q_type = forms.ChoiceField(label=_("Filtrer la recherche"), widget=forms.Select(
        attrs={'style': 'font-size: 1.1rem; width: 100%;'}), required=False, choices=QUERY_SEARCH_TYPE)


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(
            attrs={'placeholder': _('Contenu')})}


class CommentReportForm(forms.ModelForm):
    class Meta:
        model = CommentReport
        fields = ['type_alert', 'content_alert']

        widgets = {
            'type_alert': forms.Select(attrs={'style': 'width: 100%; font-size: 1.1rem;'}),
            'content_alert': forms.Textarea(attrs={'placeholder': _("Description des faits")})
        }
