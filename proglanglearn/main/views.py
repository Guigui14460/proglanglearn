from itertools import chain

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, RedirectView
from django.utils.translation import ugettext_lazy as _

from .forms import CommentReportForm
from .mixins import NavbarSearchMixin
from .models import Comment, Language, Tag


class IndexView(NavbarSearchMixin, View):
    template_name = "main/index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'navbar_search_form': self.form_navbar()})


class AboutView(NavbarSearchMixin, View):
    template_name = "main/about.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'navbar_search_form': self.form_navbar()})


class ContactView(NavbarSearchMixin, View):
    template_name = "main/contact.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'navbar_search_form': self.form_navbar()})


class TermsView(NavbarSearchMixin, View):
    template_name = "main/terms.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'navbar_search_form': self.form_navbar()})


class PrivacyView(NavbarSearchMixin, View):
    template_name = "main/privacy.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'navbar_search_form': self.form_navbar()})


class SearchView(NavbarSearchMixin, View):
    template_name = "main/search.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'navbar_search_form': self.form_navbar()})


class CommentReportView(NavbarSearchMixin, View):
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
                return HttpResponseRedirect(comment_obj.tutorial.get_absolute_url())
            except Exception as e:
                messages.error(request, _(
                    "Le commentaire n'a pas pu être signalé"))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['navbar_search_form'] = self.form_navbar()
        context['object'] = Comment.objects.get(id=kwargs.get('comment_id'))
        context['form'] = CommentReportForm()
        return context


class ChangeLanguageRedirectView(RedirectView):
    pass


class LanguagesTagsView(NavbarSearchMixin, View):
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
        context['navbar_search_form'] = self.form_navbar()
        context['tag'] = obj_list[0]
        return context
