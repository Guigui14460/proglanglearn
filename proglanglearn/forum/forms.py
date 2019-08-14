from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Subject, SubjectAnswer


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'content', 'languages']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _("Comment faire ... ?")}),
            'languages': forms.SelectMultiple(attrs={'size': 7, 'class': 'custom-multiple-select select-multiple__dark'}),
        }


class SubjectAnswerForm(forms.ModelForm):
    class Meta:
        model = SubjectAnswer
        fields = ['content']
