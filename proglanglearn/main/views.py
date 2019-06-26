from django.shortcuts import render
from django.views.generic import View

from .mixins import NavbarSearchMixin


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
