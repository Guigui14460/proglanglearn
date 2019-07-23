from django import forms
from django.utils.translation import ugettext as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from courses.models import Course, Tutorial
from .models import Question


class QuestionForm(forms.Form):
    captcha = ReCaptchaField(score_threshold=0.5)

    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answer()]
        self.fields['answer'] = forms.ChoiceField(choices=choice_list, widget=forms.RadioSelect)
