from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from .forms import LoginForm, SignUpForm, PasswordResetForm
from .models import Profile
from .utils import check_level, get_user_type
from .tokens import AccountActivationTokenGenerator
from main.mixins import NavbarSearchMixin
from main.utils import get_ip_address_client

User = get_user_model()


class CustomLoginView(NavbarSearchMixin, LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('courses:list')
        return super(CustomLoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user = request.user
        if user.is_authenticated and user.ip_address != None and get_ip_address_client(request) != user.ip_address:
            try:
                current_site = get_current_site(request)
                subject = _(
                    "Suspicion de compromission de votre compte ProgLangLearn")
                message = render_to_string('accounts/ip_address_email.html', {
                    'protocol': settings.PROTOCOL,
                    'domain': current_site.domain,
                })
                msg = EmailMultiAlternatives(
                    subject, message, "proglanglearn@gmail.com", to=[user.email])
                msg.send()
            except:
                pass
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class RegistrationView(NavbarSearchMixin, View):
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('courses:list')
        context = {'navbar_search_form': self.form_navbar()}
        context['form'] = SignUpForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.ip_address = get_ip_address_client(request)
                user.save()
                current_site = get_current_site(request)
                generator = AccountActivationTokenGenerator()
                subject = _("Activez votre compte ProgLangLearn")
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'protocol': settings.PROTOCOL,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generator.make_token(user),
                })
                msg = EmailMultiAlternatives(
                    subject, message, "proglanglearn@gmail.com", to=[user.email])
                msg.send()
                messages.success(request, _(
                    f"Envoi du mail d'activation du compte {user.username} effectué avec succès"))
            except:
                messages.warning(request, _(
                    "Échec de l'envoi de l'email d'activation"))
                return render(request, self.template_name, {
                    'form': form,
                    'navbar_search_form': self.form_navbar()
                })
            return redirect('accounts:account_activation_sent')
        users = User.objects.filter(
            username=form.data['username'], email=form.data['email'])
        if users.exists():
            user = users.first()
            if not user.profile.email_confirmed:
                user.set_password(form.clean_password2())
                user.save()
                try:
                    current_site = get_current_site(request)
                    generator = AccountActivationTokenGenerator()
                    subject = _("Activez votre compte ProgLangLearn")
                    message = render_to_string('registration/account_activation_email.html', {
                        'user': user,
                        'protocol': settings.PROTOCOL,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generator.make_token(user),
                    })
                    msg = EmailMultiAlternatives(
                        subject, message, "proglanglearn@gmail.com", to=[user.email])
                    msg.send()
                    messages.warning(request, _(
                        f"Votre compte existait déjà mais n'a pas été activé. Envoi du mail d'activation du compte {user.username} effectué avec succès"))
                except:
                    messages.warning(request,
                                     _("Échec de l'envoi de l'email d'activation"))
                    return render(request, self.template_name, {
                        'form': form,
                        'navbar_search_form': self.form_navbar()
                    })
                return redirect('accounts:account_activation_sent')
            else:
                messages.info(request, _(
                    "Votre compte a déjà été activé. Connectez-vous ou demandez à changer de mot de passe"))
                return redirect('accounts:login')
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
        if request.user.is_authenticated:
            return redirect('courses:list')
        return render(request, self.template_name, {'navbar_search_form': self.form_navbar()})


class ActivateView(View):
    template_name = 'registration/account_activation_invalid.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        generator = AccountActivationTokenGenerator()
        if user is not None and generator.check_token(user, token) and not user.profile.email_confirmed:
            user.profile.email_confirmed = True
            user.profile.save()
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, _(
                "Activation de votre compte effectuée avec succès"))
            return redirect('main:index')
        return render(request, self.template_name)


class CustomPasswordResetView(NavbarSearchMixin, PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class CustomPasswordResetDoneView(NavbarSearchMixin, PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class CustomPasswordResetConfirmView(NavbarSearchMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class = PasswordResetForm
    # post_reset_login = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class CustomPasswordResetCompleteView(NavbarSearchMixin, PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        return context


class PandasTestView(NavbarSearchMixin, View):
    template_name = 'accounts/pandas.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = self.get_context_data(**kwargs)
            context['check'] = check_level(request)
            return render(request, self.template_name, context)
        return redirect('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['navbar_search_form'] = self.form_navbar()
        return context
