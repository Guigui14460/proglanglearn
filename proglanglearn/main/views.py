from itertools import chain

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, View, ListView

from articles.models import Article
from courses.models import Course, Tutorial
from forum.models import Subject
from .forms import CommentReportForm, SearchForm, NavbarSearchForm, ContactForm, BugForm
from .mixins import NavbarSearchMixin
from .models import Comment, Language, Tag, CommentReport


User = get_user_model()


class IndexView(NavbarSearchMixin, TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_courses'] = Course.objects.get_published_courses()[:3]
        return context


class AboutView(NavbarSearchMixin, TemplateView):
    template_name = "main/about.html"


class ContactView(NavbarSearchMixin, View):
    template_name = "main/contact.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        context['bug_form'] = BugForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contact_form = ContactForm(request.POST or None)
        bug_form = BugForm(request.POST or None)
        if contact_form.is_valid():
            if not request.user.is_authenticated:
                messages.error(request, _(
                    "Vous devez être connecté pour envoyer votre message"))
            else:
                body = contact_form.cleaned_data['body'] + \
                    f"\n\n{request.user.username} ({request.user.id}) --- {request.user.email}"
                send_mail(
                    contact_form.cleaned_data['subject'],
                    body,
                    "Request Contact <proglanglearn@gmail.com>",
                    [user.email for user in User.objects.filter(is_staff=True)]
                )
                messages.success(request, _("Votre message a été envoyé"))
                contact_form = ContactForm()
            context['contact_form'] = contact_form
            context['bug_form'] = BugForm()
            return render(request, self.template_name, context)
        if bug_form.is_valid():
            send_mail(
                bug_form.cleaned_data['b_subject'],
                bug_form.cleaned_data['b_body'],
                "Bug Report <proglanglearn@gmail.com>",
                [user.email for user in User.objects.filter(is_superuser=True)]
            )
            messages.info(request, _("Votre rapport d'erreur a été envoyé"))
            bug_form = BugForm()
            context['contact_form'] = ContactForm()
            context['bug_form'] = bug_form
            return render(request, self.template_name, context)
        context['contact_form'] = contact_form
        context['bug_form'] = bug_form
        return render(request, self.template_name, context)


class TermsView(NavbarSearchMixin, TemplateView):
    template_name = "main/terms.html"


class PrivacyView(NavbarSearchMixin, TemplateView):
    template_name = "main/privacy.html"


class SearchView(NavbarSearchMixin, ListView):
    template_name = "main/search.html"
    paginate_by = 40
    type_query = 'A'
    main_query = None
    navbar_query = None
    query = None
    count = 0

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        if form.is_valid():
            self.type_query = form.cleaned_data['q_type'] if form.cleaned_data['q_type'] != '' else 'A'
            self.main_query = form.cleaned_data['q2']
        self.navbar_query = request.GET.get('q')
        self.query = self.main_query or self.navbar_query
        form = SearchForm({'q2': self.query, 'q_type': self.type_query})
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['object_list'] = self.get_queryset()
        context['count'] = self.count
        return context

    def get_queryset(self):
        request = self.request
        if self.query is not None:
            if self.type_query == 'A':
                article_results = Article.objects.search(self.query)
                course_results = Course.objects.search(self.query)
                tutorial_results = Tutorial.objects.search(self.query)
                subject_results = Subject.objects.search(self.query)
                language_results = Language.objects.search(self.query)
                tag_results = Tag.objects.search(self.query)
                qs = chain(article_results, course_results,
                           tutorial_results, subject_results,
                           language_results, tag_results)
            elif self.type_query == 'B':
                qs = Course.objects.search(self.query)
            elif self.type_query == 'C':
                qs = Tutorial.objects.search(self.query)
            elif self.type_query == 'D':
                qs = Article.objects.search(self.query)
            elif self.type_query == 'E':
                qs = Subject.objects.search(self.query)
            elif self.type_query == 'F':
                language_results = Language.objects.search(self.query)
                tag_results = Tag.objects.search(self.query)
                qs = chain(language_results, tag_results)
            else:
                qs = Article.objects.none()
            qs = sorted(qs, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        return Article.objects.none()


class CommentReportView(NavbarSearchMixin, TemplateView):
    template_name = 'main/report.html'

    def get(self, request, *args, **kwargs):
        comment_obj = get_object_or_404(
            Comment, id=kwargs.get('comment_id'))
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = CommentReportForm(request.POST or None)
        if form.is_valid():
            user = request.user
            if not user.is_authenticated:
                user = None
            comment_obj = get_object_or_404(
                Comment, id=kwargs.get('comment_id'))
            try:
                report = form.save(commit=False)
                report.comment = comment_obj
                report.alerter = user
                report.save()
                messages.success(request, _("Le commentaire a été signalé"))
                return redirect('main:analytics:comment-report')
            except Exception as e:
                messages.error(request, _(
                    "Le commentaire n'a pas pu être signalé"))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Comment.objects.get(
            id=self.kwargs.get('comment_id'))
        context['form'] = CommentReportForm()
        return context


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_id'))
        report_qs = CommentReport.objects.filter(comment=comment)
        if request.user == comment.author and not report_qs.exists():
            for reply in comment.children:
                reply.delete()
            comment.delete()
            messages.info(request, _(
                "Votre commentaire et les réponses sont supprimés"))
        else:
            messages.warning(request, _(
                "Vous ne pouvez pas supprimer ou modifier ce commentaire"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LanguagesTagsView(NavbarSearchMixin, TemplateView):
    template_name = "main/tag.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_lang = Language.objects.filter(slug=self.kwargs.get('slug'))
        obj_tag = Tag.objects.filter(slug=self.kwargs.get('slug'))
        obj_list = list(chain(obj_lang, obj_tag))
        if obj_list == []:
            raise Http404
        context['tag'] = obj_list[0]
        return context
