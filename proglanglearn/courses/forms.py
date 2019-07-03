from django import forms
from django.utils.translation import gettext_lazy as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from tinymce.widgets import TinyMCE

from accounts.models import Language, Tag
from .models import Course, Tutorial, TutorialComment


class CourseModelForm(forms.ModelForm):
    title = forms.CharField(label=_("Titre du cours"), required=True, widget=forms.TextInput(attrs={
        'placeholder': _("Gestionnaire de ...")
    }))
    thumbnail = forms.ImageField(label=_("Vignette/vidéo introduction du cours"), required=True, widget=forms.ClearableFileInput(attrs={
        'class': 'btn btn__block',
    }))
    content_introduction = forms.CharField(label=_("Intoduction/explication"), required=True, widget=TinyMCE(attrs={
        'placeholder': _("Introduction au cours")
    }))
    languages = forms.ModelMultipleChoiceField(label=_("Langages utilisés dans le cours"), required=True, widget=forms.SelectMultiple(attrs={
        'size': '7'
    }), queryset=Language.objects.all())
    tags = forms.ModelMultipleChoiceField(label=_("Catégorie"), required=False, widget=forms.SelectMultiple(attrs={
        'size': '7'
    }), queryset=Tag.objects.all(), help_text=_("S'il manque une catégorie, demandez à le <a href='contact.html#subject'>rajouter</a>. Un mail vous sera envoyer pour vous mettre au courant du rajout ou du rejet de votre demande"))
    pdf = forms.FileField(label=_("Version PDF du cours"), required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'btn btn__block btn__dark'
    }))
    published_date = forms.DateField(required=True, label=_("Date de publication du cours"), widget=forms.DateInput(
        attrs={'type': 'date'}), help_text=_(
        "Conseil : mettre une période de deux semaines en plus en attente de vérification de la part de l'administration"))
    old_price = forms.DecimalField(label=_("Prix (ou ancien si nouveau)"), required=True, widget=forms.NumberInput(attrs={
        'step': 'any',
        'min': 0
    }))
    new_price = forms.DecimalField(label=_("Nouveau prix"), required=False, widget=forms.NumberInput(attrs={
        'step': 'any',
        'min': 0
    }))
    captcha = ReCaptchaField(score_threshold=0.5)

    class Meta:
        model = Course
        fields = [
            'title', 'thumbnail', 'languages',
            'tags', 'content_introduction', 'pdf',
            'difficulty',
            'published_date', 'old_price', 'new_price'
        ]


class TutorialModelForm(forms.ModelForm):
    title = forms.CharField(label=_("Title du tutoriel"), required=True, widget=forms.TextInput(attrs={
        'placeholder': _("Gestionnaire de ...")
    }))
    content = forms.CharField(label=_("Contenu du tutoriel"), required=True, widget=TinyMCE(attrs={
        'placeholder': _("Contenu")
    }))
    resources = forms.FileField(label=_("Ressources à déposer"), required=False, widget=forms.FileInput(attrs={
        'class': 'btn btn__block btn__dark'
    }))
    experience = forms.IntegerField(label=_(
        "Points d'expérience fournis"), required=True, widget=forms.NumberInput(attrs={
            'min': 0,
            'step': 5,
        }))

    class Meta:
        model = Tutorial
        fields = [
            'title', 'content',
            'resources', 'experience',
        ]


class TutorialCommentForm(forms.ModelForm):
    content = forms.CharField(label=_("Commantaire ou réponse"), required=True, widget=forms.Textarea(attrs={
        'placeholder': _("Contenu")
    }))

    class Meta:
        model = TutorialComment
        fields = ['content']
