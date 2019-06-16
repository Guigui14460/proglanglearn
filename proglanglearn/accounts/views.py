from django.contrib import messages
from django.contrib.auth import login, get_user_model
# from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, DeleteView, View, CreateView

from .forms import LoginForm, SignUpForm, PasswordResetForm
from .models import Profile
from .tokens import AccountActivationTokenGenerator
from main.mixins import NavbarSearchMixin

User = get_user_model()


class CustomLoginView(NavbarSearchMixin, LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class RegistrationView(NavbarSearchMixin, View):
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        context = {'navbar_search_form': self.form_navbar()}
        context['form'] = SignUpForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            try:
                current_site = get_current_site(request)
                generator = AccountActivationTokenGenerator()
                subject = _("Activez votre compte ProgLangLearn")
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'protocol': 'http',  # ou https
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generator.make_token(user),
                })
                # user.email_user(subject, message)
                msg = EmailMultiAlternatives(
                    subject, message, "proglanglearn@gmail.com", to=[user.email])
                msg.send()
                messages.success(request, _(
                    f"Envoi du mail d'activation du compte {user.username} envoyé avec succès"))
            except:
                messages.warning(_("Échec de l'envoi de l'email d'activation"))
                return render(request, self.template_name, {
                    'form': form,
                    'navbar_search_form': self.form_navbar()
                })
            return HttpResponseRedirect(reverse('accounts:account_activation_sent'))
        messages.error(request, _(
            "Veuillez respecter et remplir correctement <strong>TOUS</strong> les champs obligatoires"))
        context = {
            'form': form,
            'navbar_search_form': self.form_navbar()
        }
        return render(request, self.template_name, context)


class AccountActivationSentView(NavbarSearchMixin, View):
    template_name = "registration/account_activation_sent.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'navbar_search_form': self.form_navbar()})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    generator = AccountActivationTokenGenerator()
    if user is not None and generator.check_token(user, token) and not user.is_active:
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, _(
            "Activation de votre compte effectuée avec succès"))
        return HttpResponseRedirect(reverse('main:index'))
    return render(request, 'registration/account_activation_invalid.html')


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class = PasswordResetForm
    # post_reset_login = True
