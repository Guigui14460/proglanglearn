from .forms import NavbarSearchForm


class NavbarSearchMixin(object):
    model = None

    def form_navbar(self):
        form = NavbarSearchForm()
        if form.is_valid():
            form = NavbarSearchForm(q=form.cleaned_data.get('q'))
        return form
