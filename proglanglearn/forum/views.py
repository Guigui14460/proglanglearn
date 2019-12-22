from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, RedirectView, View

from main.mixins import NavbarSearchMixin
from main.models import Language, Tag
from .forms import SubjectForm, SubjectAnswerForm
from .mixins import SubjectObjectMixin, UserCanModifySubject
from .models import Subject, SubjectAnswer


class SubjectListView(NavbarSearchMixin, ListView):
    template_name = 'forum/forum_list.html'
    queryset = Subject.objects.get_published_subjects()
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'subject-list'
        context['last_subjects'] = Subject.objects.get_last_subjects(3)
        context['tags_used'] = self.get_most_used_tags()
        return context

    def get_most_used_tags(self):
        languages = [lang for lang in Language.objects.all()
                     if lang.subject.count() > 0]
        languages.sort(key=lambda item: item.subject.count(), reverse=True)
        return languages[:5]


class SubjectDetailView(SubjectObjectMixin, NavbarSearchMixin, DetailView):
    template_name = 'forum/forum_detail.html'

    def get(self, request, *args, **kwargs):
        subject = self.get_object()
        self.object = subject
        subject.views += 1
        subject.save()
        return super(SubjectDetailView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = SubjectAnswerForm(request.POST or None)
        if form.is_valid() and request.user.is_authenticated:
            instance = form.save(commit=False)
            instance.subject = self.object
            instance.user = request.user
            instance.save()
            form = SubjectAnswerForm()
        if request.is_ajax():
            context = self.get_context_data(**kwargs)
            context['form'] = form
            html = render_to_string(
                'forum/includes/subject_comments.html', context, request=request)
            return JsonResponse({'html': html})
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CODE_COLOURS'] = settings.CODE_COLOURS
        context['form'] = SubjectAnswerForm()
        context['last_subjects'] = Subject.objects.get_last_subjects(3)
        context['tags_used'] = self.get_most_used_tags()
        return context

    def get_most_used_tags(self):
        languages = [lang for lang in Language.objects.all()
                     if lang.subject.count() > 0]
        languages.sort(key=lambda item: item.subject.count(), reverse=True)
        return languages[:5]


class SubjectFavoriteToggleRedirectView(LoginRequiredMixin, SubjectObjectMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            if obj in user.profile.favorite_subjects.all():
                user.profile.favorite_subjects.remove(obj)
            else:
                user.profile.favorite_subjects.add(obj)
        return obj.get_absolute_url()


class SubjectCreateView(LoginRequiredMixin, NavbarSearchMixin, View):
    template_name = 'forum/forum_create.html'
    success_message = _("Sujet ajouté avec succès au forum")
    error_message = _(
        "Un problème est survenu ! Réessayez plus tard et si le problème persiste, contactez l'administration")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SubjectForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            messages.success(request, self.success_message)
            return redirect('forum:subject-detail', id=instance.id)
        messages.error(request, self.error_message)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'add'
        context['form'] = SubjectForm()
        return context


class SubjectAnswerLikeToggleRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(SubjectAnswer, id=kwargs.get('answer_id'))
        parent_obj = get_object_or_404(Subject, id=kwargs.get('subject_id'))
        if obj.subject != parent_obj:
            raise Http404
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
                obj.user.profile.level_experience += 1
                obj.user.profile.save()
            else:
                obj.likes.add(user)
                obj.user.profile.level_experience -= 1
                obj.user.profile.save()
        return parent_obj.get_absolute_url()


class SubjectBestAnswerToggleRedirectView(LoginRequiredMixin, SubjectObjectMixin, UserCanModifySubject, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        answer = get_object_or_404(SubjectAnswer, id=kwargs.get('answer_id'))
        obj = self.get_object()
        if obj != answer.subject:
            raise Http404
        user = self.request.user
        if user.is_authenticated:
            if obj.closed:
                obj.closed = False
                answer.best_answer = False
                answer.user.profile.level_experience += 100
            else:
                obj.closed = True
                answer.best_answer = True
                answer.user.profile.level_experience -= 100
            obj.save()
            answer.save()
            answer.user.profile.save()
        return obj.get_absolute_url()
