from django import forms
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

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
        label = {
            'timestamp': _("Parution de l'article"),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _("Une IA fait son propre code !! OMG it's so amaziinngg !!")}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'btn btn__block'}),
            'content': TinyMCE(attrs={'placeholder': _('Corps de l\'article')}),
            'languages': forms.SelectMultiple(attrs={'size': 7, 'class': 'custom-multiple-select select-multiple__dark'}),
            'tags': forms.SelectMultiple(attrs={'size': 7, 'class': 'custom-multiple-select select-multiple__light'}),
            'timestamp': forms.DateInput(attrs={'type': 'date'}),
        }
        help_text = {
            'tags': _("S'il manque une catégorie, demandez à le <a href='#'>rajouter</a>. Un mail vous sera envoyer pour vous mettre au courant du rajout ou du rejet de votre demande"),
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
            'languages': forms.SelectMultiple(attrs={'size': 7, 'class': 'custom-multiple-select select-multiple__dark'}),
            'tags': forms.SelectMultiple(attrs={'size': 7, 'class': 'custom-multiple-select select-multiple__light'}),
        }
        help_text = {
            'tags': _("S'il manque une catégorie, demandez à le <a href='#'>rajouter</a>. Un mail vous sera envoyer pour vous mettre au courant du rajout ou du rejet de votre demande"),
        }
