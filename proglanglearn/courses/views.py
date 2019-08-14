from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, DetailView, ListView, RedirectView, UpdateView, View

from analytics.utils import save_user_exp
from main.forms import CommentModelForm
from main.mixins import NavbarSearchMixin
from main.models import Comment
from main.signals import comment_signal
from .forms import CourseModelForm, CourseUpdateModelForm, TutorialModelForm
from .mixins import CourseObjectMixin, TutorialObjectMixin, UserCanAddCourse, UserCanModifyCourse, UserCanViewTutorial
from .models import Course, Tutorial
from .utils import send_email_new_course


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
                "Cours \"%(course_title)s\" ajouté avec succès") % {'course_title': course.title})
            return redirect('courses:list')
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'create'
        context['type'] = 'add'
        return context


class CourseDetailView(CourseObjectMixin, NavbarSearchMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            ternary = True if self.request.user in self.get_object(
            ).students.all() or self.request.user == self.get_object().author or self.request.user.is_staff else False
        except:
            ternary = False
        context['can_view'] = ternary
        return context


class CourseListView(NavbarSearchMixin, ListView):
    queryset = Course.objects.get_published_courses()
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        default = super().get(request, *args, **kwargs)
        course_email_to_send = Course.objects.get_send_email_course()
        for course in course_email_to_send:
            send_email_new_course(request, course)
        course_email_to_send.update(email_send=True)
        return default

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'list'
        return context


class CourseUpdateView(LoginRequiredMixin, CourseObjectMixin, UserCanModifyCourse, SuccessMessageMixin, NavbarSearchMixin, UpdateView):
    template_name = 'courses/course_create.html'
    form_class = CourseUpdateModelForm
    success_message = _("Cours modifié avec succès")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'modify'
        context['tutorials'] = self.get_object().get_tutorials()
        return context

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'slug': self.get_object().slug})


class CourseDeleteView(LoginRequiredMixin, CourseObjectMixin, SuccessMessageMixin, NavbarSearchMixin, DeleteView):
    success_message = _("Cours supprimé avec succès")
    success_url = reverse_lazy('courses:list')


class CourseUserEnrolledView(LoginRequiredMixin, CourseObjectMixin, SuccessMessageMixin, View):
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if user in course.students.all() or user.is_staff or user == course.author:
            messages.info(request, _("Vous êtes déjà inscrit au cours"))
            return redirect('courses:tutorial-detail', course_slug=course.slug, tutorial_slug=course.tutorial.first().slug)
        else:
            if course.old_price == 0 or (course.new_price is not None and course.new_price == 0):
                course.students.add(request.user)
                messages.info(request, _("Bienvenue au cours : %(course_title)s") % {
                              'course_title': course.title})
                return redirect('courses:tutorial-detail', course_slug=course.slug, tutorial_slug=course.tutorial.first().slug)
            return redirect('main:billing:add-course', course_slug=course.slug)


class TutorialCreateView(LoginRequiredMixin, NavbarSearchMixin, View):
    template_name = 'courses/tutorial_create.html'
    success_message = _("Tutoriel ajouté avec succès")

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs.get('course_slug'))
        if request.user != course.author and not request.user.is_staff:
            messages.warning(request, _(
                "Vous ne pouvez pas créer un tutoriel car vous ne faîtes pas partie de l'administration de ProgLangLearn ou vous n'êtes pas l'auteur du cours"))
            return redirect('courses:detail', slug=course.slug)
        context = self.get_context_data(**kwargs)
        context['form'] = TutorialModelForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs.get('course_slug'))
        form = TutorialModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.course = course
            tutorial.published_date = timezone.now()
            tutorial.save()
            return redirect('courses:tutorial-detail', course_slug=course.slug, tutorial_slug=tutorial.slug)
        return redirect('courses:update', slug=course.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'add'
        context['course'] = Course.objects.get(
            slug=self.kwargs.get('course_slug'))
        return context


class TutorialDetailView(LoginRequiredMixin, UserCanViewTutorial, TutorialObjectMixin, NavbarSearchMixin, DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        tutorial = self.get_object()
        tutorial.views = F('views') + 1
        tutorial.save()
        user = request.user
        if user.is_authenticated:
            tuto_finished = user.profile.tutorial_finished.all()
            if not tutorial in tuto_finished:
                user.profile.tutorial_finished.add(tutorial)
                user.profile.level_experience += tutorial.experience
                user.profile.save()
                save_user_exp(request, tutorial.experience)
        return super(TutorialDetailView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentModelForm(request.POST or None)
        if form.is_valid() and request.user.is_authenticated:
            content = form.cleaned_data['content']
            parent_id = request.POST.get('parent_id')
            instance = self.object
            if parent_id:
                instance = Comment.objects.get(id=parent_id)
            comment_signal.send(instance.__class__,
                                instance=instance, request=request)
        if request.is_ajax():
            context = self.get_context_data(**kwargs)
            context['form'] = form
            html = render_to_string(
                'main/includes/comments.html', context, request=request)
            return JsonResponse({'html': html, 'comments_count': context['parent_comments'].count()})
        return self.get(request, *args, **kwargs)

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
        context['form'] = CommentModelForm()
        instance = self.get_object()
        c_type = ContentType.objects.get_for_model(instance)
        context['parent_comments'] = Comment.objects.filter(
            content_type=c_type, object_id=instance.id, reported=False).order_by('timestamp')
        return context


class TutorialFavoriteToggleRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Tutorial, slug=kwargs.get('tutorial_slug'))
        user = self.request.user
        if user.is_authenticated:
            if obj in user.profile.favorite_tutorials.all():
                user.profile.favorite_tutorials.remove(obj)
            else:
                user.profile.favorite_tutorials.add(obj)
        return obj.get_absolute_url()


class TutorialUpdateView(LoginRequiredMixin, TutorialObjectMixin, UserCanModifyCourse, SuccessMessageMixin, NavbarSearchMixin, UpdateView):
    template_name = 'courses/tutorial_create.html'
    form_class = TutorialModelForm
    success_message = _("Tutoriel modifié avec succès")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'modify'
        context['course'] = Course.objects.get(
            slug=self.kwargs.get('course_slug'))
        return context

    def get_success_url(self):
        return reverse('courses:tutorial-detail', kwargs={'course_slug': self.get_object().course.slug, 'tutorial_slug': self.get_object().slug})


class TutorialDeleteView(LoginRequiredMixin, TutorialObjectMixin, SuccessMessageMixin, NavbarSearchMixin, DeleteView):
    success_message = _("Cours supprimé avec succès")

    def get_success_url(self):
        course_slug = self.kwargs.get('course_slug')
        return reverse('courses:detail', kwargs={'slug': course_slug})
