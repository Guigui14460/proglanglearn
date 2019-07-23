from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DeleteView, DetailView, ListView, RedirectView, UpdateView, View
from django.views.generic.base import TemplateView


class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'billing/payment.html'
