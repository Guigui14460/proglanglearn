from django import forms
from django.utils.translation import ugettext as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from tinymce.widgets import TinyMCE

from main.models import Language, Tag
from .models import Article


class ArticleModelForm(forms.ModelForm):
    captcha = ReCaptchaField(score_threshold=0.5)

    class Meta:
        model = Article
        fields = [
            'title', 'thumbnail', 'languages', 'tags', 'content', 'timestamp'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _("Une IA fait son propre code !! OMG it's so amaziinngg !!")}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'btn btn__block'}),
            'content': TinyMCE(attrs={'placeholder': _('Corps de l\'article')}),
            'languages': forms.SelectMultiple(attrs={'size': 7}),
            'tags': forms.SelectMultiple(attrs={'size': 7}),
            'timestamp': forms.DateInput(attrs={'type': 'date'}),
        }
        help_text = {
            'tags': _("S'il manque une catégorie, demandez à le <a href='contact.html#subject'>rajouter</a>. Un mail vous sera envoyer pour vous mettre au courant du rajout ou du rejet de votre demande"),
        }


class ArticleUpdateModelForm(forms.ModelForm):
    captcha = ReCaptchaField(score_threshold=0.5)

    class Meta:
        model = Article
        fields = [
            'title', 'thumbnail', 'languages', 'tags', 'content'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _("Une IA fait son propre code !! OMG it's so amaziinngg !!")}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'btn btn__block'}),
            'content': TinyMCE(attrs={'placeholder': _('Corps de l\'article')}),
            'languages': forms.SelectMultiple(attrs={'size': 7}),
            'tags': forms.SelectMultiple(attrs={'size': 7}),
        }
        help_text = {
            'tags': _("S'il manque une catégorie, demandez à le <a href='contact.html#subject'>rajouter</a>. Un mail vous sera envoyer pour vous mettre au courant du rajout ou du rejet de votre demande"),
        }
