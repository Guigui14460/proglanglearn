from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.shortcuts import reverse, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, View

from main.mixins import NavbarSearchMixin
from .forms import CourseModelForm, TutorialModelForm
from .mixins import CourseObjectMixin, TutorialObjectMixin, UserCanAddCourse, UserCanModifyCourse, UserCanViewTutorial
from .models import Course, Tutorial


class CourseCreateView(LoginRequiredMixin, UserCanAddCourse, NavbarSearchMixin, View):
    template_name = 'courses/course_create.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = CourseModelForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = CourseModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            course = form.save(commit=False)
            user = request.user
            course.author = user
            form.save()
            messages.success(request, _(
                f"Cours \"{course.title}\" ajouté avec succès"))
            return redirect('courses:list')
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['activate'] = 'create'
        context['title'] = _("Ajouter")
        context['navbar_search_form'] = self.form_navbar()
        return context


class CourseDetailView(CourseObjectMixin, NavbarSearchMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            ternary = True if self.request.user.profile in self.get_object(
            ).students.all() or self.request.user == self.get_object().author or self.request.user.is_staff else False
        except:
            ternary = False
        context['can_view'] = ternary
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


class CourseUpdateView(LoginRequiredMixin, CourseObjectMixin, UserCanModifyCourse, SuccessMessageMixin, NavbarSearchMixin, UpdateView):
    template_name = 'courses/course_create.html'
    form_class = CourseModelForm
    success_message = _("Cours modifié avec succès")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Modifier")
        context['tutorials'] = self.get_object().get_tutorials()
        context['navbar_search_form'] = self.form_navbar()
        return context

    def get_success_url(self):
        id_ = self.kwargs.get('id')
        return reverse('courses:detail', kwargs={'id': id_})


class CourseDeleteView(LoginRequiredMixin, CourseObjectMixin, SuccessMessageMixin, NavbarSearchMixin, DeleteView):
    success_message = _("Cours supprimé avec succès")
    success_url = reverse_lazy('courses:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class CourseUserEnrolledView(LoginRequiredMixin, CourseObjectMixin, SuccessMessageMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if user.profile in course.students.all():
            messages.info(request, _("Vous êtes déjà inscrit au cours"))
        else:
            course.students.add(user.profile)
            messages.success(request, _(
                f"Bienvenue au cours : {course.title}"))
        return redirect('courses:tutorial-detail', course_id=course.id, tutorial_id=course.tutorial.first().id)


class TutorialCreateView(LoginRequiredMixin, NavbarSearchMixin, View):
    template_name = 'courses/tutorial_create.html'
    success_message = _("Tutoriel ajouté avec succès")

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs.get('course_id'))
        if request.user != course.author and not request.user.is_staff:
            messages.warning(request, _(
                "Vous ne pouvez pas créer un tutoriel car vous ne faîtes pas partie de l'administration de ProgLangLearn ou vous n'êtes pas l'auteur du cours"))
            return redirect('courses:detail', id=course.id)
        context = self.get_context_data(**kwargs)
        context['form'] = TutorialModelForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs.get('course_id'))
        form = TutorialModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.course = course
            tutorial.published_date = timezone.now()
            tutorial.save()
            return redirect('courses:tutorial-detail', course_id=course.id, tutorial_id=tutorial.id)
        return redirect('courses:update', id=course.id)

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['title'] = _("Ajouter")
        context['course'] = Course.objects.get(id=self.kwargs.get('course_id'))
        context['navbar_search_form'] = self.form_navbar()
        return context


class TutorialDetailView(UserCanViewTutorial, TutorialObjectMixin, NavbarSearchMixin, DetailView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('tutorial_id')
        tutorial = Tutorial.objects.get(id=id)
        tutorial.views = F('views') + 1
        tutorial.save()
        user = request.user
        tuto_finished = user.profile.tutorial_finished
        if not tutorial.id in [int(tut) for tut in tuto_finished]:
            tuto_finished += [tutorial.id]
            user.profile.tutorial_finished = tuto_finished
            user.profile.level_experience += tutorial.experience
            user.profile.save()
        return super(TutorialDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_tutorials'] = self.get_other_tutorial()
        for i, tut in enumerate(context['course_tutorials']):
            if tut == self.get_object():
                try:
                    context['prev_tutorial'] = context['course_tutorials'][i - 1]
                except:
                    context['prev_tutorial'] = None
                try:
                    context['next_tutorial'] = context['course_tutorials'][i + 1]
                except:
                    context['next_tutorial'] = None
        context['navbar_search_form'] = self.form_navbar()
        return context
