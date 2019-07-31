from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, DetailView, ListView, RedirectView, UpdateView, View

from courses.mixins import UserCanAddCourse, UserCanModifyCourse
from main.mixins import NavbarSearchMixin
from .forms import QuestionForm
from .mixins import QuizObjectMixin, UserCanAnswerQuiz
from .models import Sitting


class QuizDetailView(LoginRequiredMixin, UserCanAnswerQuiz, QuizObjectMixin, DetailView):
    pass
