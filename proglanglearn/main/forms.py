from django import forms
from django.utils.translation import ugettext as _

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
            'type_alert': forms.Select(),
            'content_alert': forms.Textarea(attrs={'placeholder': _("Description des faits")})
        }
