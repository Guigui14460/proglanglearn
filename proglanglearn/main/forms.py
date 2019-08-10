from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment, CommentReport


class NavbarSearchForm(forms.Form):
    q = forms.CharField(label=_("Recherche"), widget=forms.TextInput(attrs={
        'id': 'search',
        'placeholder': _("Recherche"),
        'name': 'q'
    }), required=False)


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
