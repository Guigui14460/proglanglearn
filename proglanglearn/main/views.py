from django.shortcuts import render
from django.views.generic import View

from .mixins import NavbarSearchMixin


class IndexView(NavbarSearchMixin, View):
    template_name = "main/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'navbar_search_form': self.form_navbar()})


def contact(request):
    return render(request, 'main/contact.html')


def terms(request):
    # form = NavbarSearchForm()
    # qs = []
    # if form.is_valid():
    #     qs = Profile.objects.all()
    #     form = NavbarSearchForm()
    # context = {'form': form, 'objects': qs}
    return render(request, 'main/terms.html', {})


def about(request):
    return render(request, 'main/about.html')


def privacy(request):
    return render(request, 'main/privacy.html')


def search(request):
    return render(request, "main/search.html")


def error_403(request, exception):
    return render(request, '403.html', {})


def error_404(request, exception):
    return render(request, '404.html', {})


def error_500(request):
    return render(request, '500.html', {})
