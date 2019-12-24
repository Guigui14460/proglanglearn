from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _, activate, get_language
from django.views.generic import View, TemplateView, ListView

from allauth.account.views import PasswordChangeView

from main.mixins import NavbarSearchMixin
from main.utils import get_ip_address_client
from .allauth_forms import (
    ChangePasswordForm as PasswordChangeForm
)
from .forms import (
    LoginForm, 
    SignUpForm, PasswordResetForm, 
    ChangeProfileImageForm, PersonalInformationForm, 
    ProfileInformationForm, 
    DangerZoneForm, ExperienceForm, 
    EducationForm, ProfileSearchForm, 
)
from .github_backend import GithubRepo
from .mixins import UserCanModifyProfile, ProfileObjectMixin
from .models import ProgType, Profile, Education, Experience, ProfileReport
from .utils import check_level
from .tokens import AccountActivationTokenGenerator


User = get_user_model()


class CustomLoginView(NavbarSearchMixin, LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:analytics:dashboard')
        return super(CustomLoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user = request.user
        if user.is_authenticated and user.ip_address != None and get_ip_address_client(request) != user.ip_address:
            try:
                actual = get_language()
                activate(user.natural_language)
                current_site = get_current_site(request)
                subject = _(
                    "Suspicion de compromission de votre compte ProgLangLearn")
                message = render_to_string('accounts/ip_address_email.html', {
                    'protocol': settings.PROTOCOL,
                    'domain': current_site.domain,
                })
                msg = EmailMultiAlternatives(
                    subject, message, "No reply <proglanglearn@gmail.com>", to=[user.email])
                msg.send()
                activate(actual)
            except:
                pass
        return self.get(request, *args, **kwargs)


class RegistrationView(NavbarSearchMixin, View):
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:analytics:dashboard')
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
                    subject, message, "No reply <proglanglearn@gmail.com>", to=[user.email])
                msg.send()
                messages.success(request, _(
                    "Envoi du mail d'activation du compte %(username)s effectué avec succès") % {'username': user.username})
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
                        subject, message, "No reply <proglanglearn@gmail.com>", to=[user.email])
                    msg.send()
                    messages.warning(request, _(
                        "Votre compte existait déjà mais n'a pas été activé. Envoi du mail d'activation du compte %(username)s effectué avec succès") % {'username': user.username})
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
                return redirect('account_login')
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
            return redirect('account_login')
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
            return redirect('main:analytics:dashboard')
        return render(request, self.template_name)


class CustomPasswordResetView(NavbarSearchMixin, PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(NavbarSearchMixin, PasswordResetDoneView):
    pass


class CustomPasswordResetConfirmView(NavbarSearchMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class = PasswordResetForm
    post_reset_login = settings.RESET_LOGIN_AFTER_PASSWORD_RESET


class CustomPasswordResetCompleteView(NavbarSearchMixin, PasswordResetCompleteView):
    pass


class AccountView(LoginRequiredMixin, NavbarSearchMixin, View):
    template_name = 'accounts/account.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'account'
        context['image_form'] = ChangeProfileImageForm(
            instance=self.request.user.profile)
        context['personal_form'] = PersonalInformationForm(
            self.get_personal_info(), request=self.request)
        context['profile_form'] = ProfileInformationForm(
            self.get_profile_info())
        if len(self.request.user.socialaccount_set.all()) == 0:
            context['password_change_form'] = PasswordChangeForm(
                user=self.request.user)
            context['danger_zone_form'] = DangerZoneForm(user=self.request.user)
        return context

    def get_personal_info(self):
        user = self.request.user
        if user.profile.is_dev:
            prog_type = ProgType.objects.get(type_id='D')
        elif user.profile.is_student:
            prog_type = ProgType.objects.get(type_id='S')
        else:
            prog_type = ProgType.objects.get(type_id='A')
        info_dict = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email_notification': user.profile.email_notification,
            'prog_type': prog_type,
            'country': user.profile.country
        }
        return info_dict

    def get_profile_info(self):
        user = self.request.user
        links = user.profile.links.split(';')
        info_dict = {
            'skills': user.profile.languages_learnt.all(),
            'github': user.profile.github_username,
            'biography': user.profile.biography,
            'website_url': links[0],
            'youtube_url': links[1],
            'linked_in_url': links[2],
            'facebook_url': links[3],
            'twitter_url': links[4],
            'instagram_url': links[5],
        }
        return info_dict


class PersonalInfo(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        image_form = ChangeProfileImageForm(
            request.POST or None, request.FILES or None)
        personal_form = PersonalInformationForm(
            request.POST or None, request=request)
        if image_form.is_valid() and personal_form.is_valid():
            prog_type = personal_form.cleaned_data['prog_type']
            if prog_type.type_id == 'D':
                user.profile.is_dev = True
                user.profile.is_student = False
            elif prog_type.type_id == 'S':
                user.profile.is_dev = False
                user.profile.is_student = True
            else:
                user.profile.is_dev = False
                user.profile.is_student = False
            user.username = personal_form.cleaned_data['username']
            if len(user.socialaccount_set.all()) > 0:
                user.email = user.socialaccount_set.all()[0].extra_data['email']
            else:
                user.email = personal_form.cleaned_data['email']
                user.first_name = personal_form.cleaned_data['first_name']
                user.last_name = personal_form.cleaned_data['last_name'].upper()
            user.save()
            if image_form.cleaned_data['image'] != 'user_pictures/default.png':
                user.profile.image = image_form.cleaned_data['image']
            user.profile.email_notification = personal_form.cleaned_data['email_notification']
            user.profile.country = personal_form.cleaned_data['country']
            user.profile.profile_reported = False
            user.profile.save()
            messages.info(request, _(
                "Vos informations personnelles ont été mises à jour"))
        else:
            messages.warning(request, _(
                "Vos informations personnelles n'ont pas pu être modifiées. Rétablissement des anciennes informations"))
        return redirect('accounts:account')


class ChangePassword(PasswordChangeView):
    def post(self, request, *args, **kwargs):
        change_post = super().post(request, *args, **kwargs)
        # user = request.user
        # form = PasswordChangeForm(user, request.POST or None)
        # if form.is_valid():
        #     user.set_password(form.clean_new_password2())
        #     user.save()
        #     messages.success(request, _(
        #         "Votre mot de passe a été modifié avec succès"))
        # else:
        #     messages.error(request, _(
        #         "Votre mot de passe n'a pas pu être modifié. Utilisez l'aide sous chaque champs"))
        return redirect('accounts:account')
    
    def form_valid(self, form):
        return super().form_valid(form)


class ProfileInfo(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        form = ProfileInformationForm(request.POST or None)
        if form.is_valid():
            user.profile.profile_reported = False
            user.profile.biography = form.cleaned_data['biography']
            user.profile.languages_learnt.remove(
                *user.profile.languages_learnt.all())
            user.profile.languages_learnt.add(*form.cleaned_data['skills'])
            user.profile.links = f"{form.cleaned_data['website_url']};{form.cleaned_data['youtube_url']};{form.cleaned_data['linked_in_url']};{form.cleaned_data['facebook_url']};{form.cleaned_data['twitter_url']};{form.cleaned_data['instagram_url']}"
            user.profile.github_username = form.cleaned_data['github']
            user.profile.save()
            messages.info(request, _(
                "Les informations sur votre profil ont été mises à jour"))
        else:
            messages.warning(request, _(
                "Vos informations visibles de votre profil n'ont pas pu être modifiées. Rétablissement des anciennes informations"))
        return redirect('accounts:account')


class DangerZone(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        form = DangerZoneForm(user, request.POST or None)
        if form.is_valid():
            user.is_active = False
            user.save()
            logout(request)
            messages.success(request, _("Votre compte a été désactivé"))
            return redirect('account_login')
        messages.error(request, _("Votre compte n'a pas pu être désactiver"))
        return redirect('accounts:account')


class ProfileView(ProfileObjectMixin, NavbarSearchMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'profile'
        context['object'] = self.get_object()
        links = context['object'].links.split(';')
        context['media_links'] = {
            'website': links[0],
            'youtube': links[1],
            'linkedin': links[2],
            'facebook': links[3],
            'twitter': links[4],
            'instagram': links[5],
        }
        try:
            github_client = GithubRepo(context['object'].github_username)
            context['repos'] = github_client.get_repos_informations()
            for repo in context['repos']:
                repo['description'] = ' '.join(repo['description'])
        except:
            context['repos'] = []
        return context


class ProfileListView(NavbarSearchMixin, ListView):
    template_name = 'accounts/profiles.html'
    paginate_by = 20
    query = None
    count = 0

    def get(self, request, *args, **kwargs):
        form = ProfileSearchForm(request.GET)
        if form.is_valid():
            self.query = form.cleaned_data['q_profile']
        form = ProfileSearchForm({'q_profile': self.query})
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
        if self.query is not None and self.query != '':
            qs = Profile.objects.search(self.query)
        else:
            qs = Profile.objects.all_dev_student()
        self.count = len(qs)
        return qs


class ProfileEditView(LoginRequiredMixin, ProfileObjectMixin, UserCanModifyProfile, NavbarSearchMixin, TemplateView):
    template_name = 'accounts/edit_profile.html'

    def post(self, request, *args, **kwargs):
        if 'education' in request.POST:
            education_form = EducationForm(request.POST or None)
            if education_form.is_valid():
                instance = education_form.save(commit=False)
                instance.profile = request.user.profile
                instance.save()
                instance.profile.profile_reported = False
                instance.profile.save()
                education_form = EducationForm()
            if request.is_ajax():
                context = self.get_context_data(**kwargs)
                context['education_form'] = education_form
                html = render_to_string(
                    'accounts/includes/education.html', context, request=request)
                return JsonResponse({'html': html})
            messages.info(request, _("École ajoutée à votre espace éducation"))
            context = self.get_context_data(**kwargs)
            context['education_form'] = education_form
            return render(request, self.template_name, context)
        elif 'experience' in request.POST:
            experience_form = ExperienceForm(request.POST or None)
            if experience_form.is_valid():
                instance = experience_form.save(commit=False)
                instance.profile = request.user.profile
                instance.save()
                instance.profile.profile_reported = False
                instance.profile.save()
                experience_form = ExperienceForm()
            if request.is_ajax():
                context = self.get_context_data(**kwargs)
                context['experience_form'] = experience_form
                html = render_to_string(
                    'accounts/includes/experience.html', context, request=request)
                return JsonResponse({'html': html})
            messages.info(request, _("Expérience ajoutée à votre espace expérience"))
            context = self.get_context_data(**kwargs)
            context['experience_form'] = experience_form
            return render(request, self.template_name, context)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['education_form'] = EducationForm()
        context['experience_form'] = ExperienceForm()
        return context


class ProfileReportView(ProfileObjectMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, id=kwargs.get('profile_id'))
        if not profile.profile_reported:
            if request.user != profile.user:
                instance = ProfileReport.objects.create(profile=profile)
                profile.profile_reported = True
                profile.save()
                messages.info(request, _("Profil signalé"))
            else:
                messages.error(request, _("Vous ne pouvez pas vous signaler vous-même"))
        else:
            messages.warning(request, _("Le profil a déjà été signalé et est en attente de modification par le gérant de ce profil"))
        return redirect('accounts:profile', user_id=profile.user.id)


class ExperienceDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        experience = get_object_or_404(Experience, id=kwargs.get('experience_id'))
        if request.user.profile == experience.profile:
            experience.delete()
            messages.info(request, _("Expérience supprimée"))
            return redirect('accounts:profile-edit', user_id=request.user.id)
        else:
            messages.error(request, _("Vous n'avez pas l'autorisation de le supprimer"))
            return redirect('accounts:profile', user_id=experience.profile.user.id)


class EducationDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        education = get_object_or_404(Education, id=kwargs.get('education_id'))
        if request.user.profile == education.profile:
            education.delete()
            messages.info(request, _("Éducation supprimée"))
            return redirect('accounts:profile-edit', user_id=request.user.id)
        else:
            messages.error(request, _("Vous n'avez pas l'autorisation de le supprimer"))
            return redirect('accounts:profile', user_id=education.profile.user.id)
