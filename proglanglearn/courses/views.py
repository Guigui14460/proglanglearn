from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.views import NavbarSearchMixin
from .forms import CourseModelForm
from .models import Course


class CourseObjectMixin(object):
    model = Course

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class CourseCreateView(SuccessMessageMixin, NavbarSearchMixin, CreateView):
    template_name = 'courses/course_create.html'
    form_class = CourseModelForm
    queryset = Course.objects.all()
    success_message = _("Cours ajouté avec succès")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'create'
        context['title'] = _("Ajouter")
        context['navbar_search_form'] = self.form_navbar()
        return context


class CourseDetailView(CourseObjectMixin, NavbarSearchMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class CourseListView(NavbarSearchMixin, ListView):
    queryset = Course.objects.get_published_courses()
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'list'
        context['navbar_search_form'] = self.form_navbar()
        return context


class CourseUpdateView(CourseObjectMixin, SuccessMessageMixin, NavbarSearchMixin, UpdateView):
    template_name = 'courses/course_create.html'
    form_class = CourseModelForm
    success_message = _("Cours modifié avec succès")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Modifier")
        context['navbar_search_form'] = self.form_navbar()
        return context

    def get_success_url(self):
        id_ = self.kwargs.get('id')
        return reverse('courses:detail', kwargs={'id': id_})


class CourseDeleteView(CourseObjectMixin, SuccessMessageMixin, NavbarSearchMixin, DeleteView):
    success_message = _("Cours supprimé avec succès")
    success_url = reverse_lazy('courses:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context
