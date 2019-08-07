from itertools import chain

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, View

from .forms import CommentReportForm
from .mixins import NavbarSearchMixin
from .models import Comment, Language, Tag, CommentReport


class IndexView(NavbarSearchMixin, TemplateView):
    template_name = "main/index.html"


class AboutView(NavbarSearchMixin, TemplateView):
    template_name = "main/about.html"


class ContactView(NavbarSearchMixin, TemplateView):
    template_name = "main/contact.html"


class TermsView(NavbarSearchMixin, TemplateView):
    template_name = "main/terms.html"


class PrivacyView(NavbarSearchMixin, TemplateView):
    template_name = "main/privacy.html"


class SearchView(NavbarSearchMixin, TemplateView):
    template_name = "main/search.html"


class CommentReportView(NavbarSearchMixin, TemplateView):
    template_name = 'main/report.html'

    def get(self, request, *args, **kwargs):
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
        context = {**kwargs}
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
        context = {**kwargs}
        obj_lang = Language.objects.filter(slug=self.kwargs.get('slug'))
        obj_tag = Tag.objects.filter(slug=self.kwargs.get('slug'))
        obj_list = list(chain(obj_lang, obj_tag))
        if obj_list == []:
            raise Http404
        context['tag'] = obj_list[0]
        return context
