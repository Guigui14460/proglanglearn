from django import forms
from django.utils.translation import gettext_lazy as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from tinymce.widgets import TinyMCE

from main.models import Language, Tag
from .models import Course, Tutorial


class CourseModelForm(forms.ModelForm):
    captcha = ReCaptchaField(score_threshold=0.5)

    class Meta:
        model = Course
        fields = [
            'title', 'thumbnail', 'languages',
            'tags', 'content_introduction', 'pdf',
            'difficulty',
            'published_date', 'old_price', 'new_price'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _("Gestionnaire de ...")}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'btn btn__block'}),
            'content_introduction': TinyMCE(attrs={'placeholder': _('Introduction au cours')}),
            'languages': forms.SelectMultiple(attrs={'size': 7}),
            'tags': forms.SelectMultiple(attrs={'size': 7}),
            'pdf': forms.ClearableFileInput(attrs={'class': 'btn btn__block btn__dark'}),
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'old_price': forms.NumberInput(attrs={'step': 'any', 'min': 0}),
            'new_price': forms.NumberInput(attrs={'step': 'any', 'min': 0})
        }
        help_text = {
            'tags': _("S'il manque une catégorie, demandez à le <a href='contact.html#subject'>rajouter</a>. Un mail vous sera envoyer pour vous mettre au courant du rajout ou du rejet de votre demande"),
            'published_date': _("Conseil : mettre une période de deux semaines en plus en attente de vérification de la part de l'administration")
        }


class CourseUpdateModelForm(forms.ModelForm):
    captcha = ReCaptchaField(score_threshold=0.5)

    class Meta:
        model = Course
        fields = [
            'title', 'thumbnail', 'languages',
            'tags', 'content_introduction', 'pdf',
            'difficulty',
            'old_price', 'new_price'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _("Gestionnaire de ...")}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'btn btn__block'}),
            'content_introduction': TinyMCE(attrs={'placeholder': _('Introduction au cours')}),
            'languages': forms.SelectMultiple(attrs={'size': 7}),
            'tags': forms.SelectMultiple(attrs={'size': 7}),
            'pdf': forms.ClearableFileInput(attrs={'class': 'btn btn__block btn__dark'}),
            'old_price': forms.NumberInput(attrs={'step': 'any', 'min': 0}),
            'new_price': forms.NumberInput(attrs={'step': 'any', 'min': 0})
        }
        help_text = {
            'tags': _("S'il manque une catégorie, demandez à le <a href='contact.html#subject'>rajouter</a>. Un mail vous sera envoyer pour vous mettre au courant du rajout ou du rejet de votre demande"),
        }


class TutorialModelForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['title', 'content', 'resources', 'experience']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _("Installation ...")}),
            'content': TinyMCE(attrs={'placeholder': _("Contenu")}),
            'resources': forms.FileInput(attrs={'class': 'btn btn__block btn__dark'}),
            'experience': forms.NumberInput(attrs={'min': 0, 'step': 5}),
        }
