from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, DetailView, ListView, RedirectView, UpdateView, View

from main.mixins import NavbarSearchMixin
from .forms import CourseModelForm, TutorialModelForm, TutorialCommentForm, TutorialCommentReportForm
from .mixins import CourseObjectMixin, TutorialObjectMixin, UserCanAddCourse, UserCanModifyCourse, UserCanViewTutorial
from .models import Course, Tutorial, TutorialComment, TutorialCommentReport


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


class TutorialDetailView(LoginRequiredMixin, UserCanViewTutorial, TutorialObjectMixin, NavbarSearchMixin, DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        tutorial = self.get_object()
        tutorial.views = F('views') + 1
        tutorial.save()
        user = request.user
        tuto_finished = user.profile.tutorial_finished
        if tuto_finished != ['']:
            if not tutorial.id in [int(tut) for tut in tuto_finished]:
                tuto_finished += [tutorial.id]
                user.profile.tutorial_finished = tuto_finished
                user.profile.level_experience += tutorial.experience
                user.profile.save()
        else:
            tuto_finished = [tutorial.id]
            user.profile.tutorial_finished = tuto_finished
            user.profile.level_experience += tutorial.experience
            user.profile.save()
        return super(TutorialDetailView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TutorialCommentForm(request.POST or None)
        if form.is_valid() and request.user.is_authenticated:
            content = form.cleaned_data['content']
            parent_id = request.POST.get('parent_id')
            parent_qs = None
            if parent_id:
                parent_qs = TutorialComment.objects.get(id=parent_id)
            comment = TutorialComment.objects.create(
                user=request.user,
                tutorial=Tutorial.objects.get(
                    id=self.kwargs.get('tutorial_id')),
                content=content,
                parent=parent_qs
            )
        if request.is_ajax():
            context = self.get_context_data(**kwargs)
            context['form'] = form
            html = render_to_string('courses/tutorial_comments.html', context, request=request)
            return JsonResponse({'html': html})
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
        context['navbar_search_form'] = self.form_navbar()
        context['form'] = TutorialCommentForm()
        context['parent_comments'] = TutorialComment.objects.tutorial_parent_comments(self.get_object())
        context['tutorial_in_favorite'] = self.tuto_in_favorite()
        return context
    
    def tuto_in_favorite(self):
        user = self.request.user
        tuto = self.object
        liste_tuto = user.profile.favorite_tutorials
        return str(tuto.id) in liste_tuto


class TutorialFavoriteToggleRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Tutorial, id=kwargs.get('tutorial_id'))
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            tuto_list = user.profile.favorite_tutorials
            if str(obj.id) in tuto_list:
                tuto_list.remove(str(obj.id))
            else:
                tuto_list += [str(obj.id)]
            user.profile.favorite_tutorials = tuto_list
            user.profile.save()
        return url_


class TutorialCommentReportView(NavbarSearchMixin, View):
    template_name = 'courses/report.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = TutorialCommentReportForm(request.POST or None)
        if form.is_valid():
            user = request.user
            if not user.is_authenticated:
                user = None
            comment_obj = get_object_or_404(TutorialComment, id=kwargs.get('comment_id'))
            try:
                report = form.save(commit=False)
                report.comment = comment_obj
                report.alerter = user
                report.save()
                messages.success(request, _("Le commentaire a été signalé"))
                return HttpResponseRedirect(comment_obj.tutorial.get_absolute_url())
            except Exception as e:
                messages.error(request, _("Le commentaire n'a pas pu être signalé"))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['navbar_search_form'] = self.form_navbar()
        context['form'] = TutorialCommentReportForm()
        return context
