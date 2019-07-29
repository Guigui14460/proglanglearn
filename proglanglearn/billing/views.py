import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DeleteView, DetailView, ListView, RedirectView, UpdateView, View
from django.views.generic.base import TemplateView

import stripe

from courses.models import Course
from main.mixins import NavbarSearchMixin
from .forms import CheckoutForm, CouponForm, RefundForm
from .mixins import UserCanViewCheckout
from .models import Order, Coupon, Payment, Refund


User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))


class PaymentView(LoginRequiredMixin, UserCanViewCheckout, NavbarSearchMixin, View):
    template_name = 'billing/payment.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # context['form'] = CheckoutForm()
        # token = stripe.Token.create(
        #     card={
        #         'number': '4242424242424242',
        #         'exp_month': 12,
        #         'exp_year': 2010,
        #         'cvc': '123',
        #     },
        # )
        # print(token)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        token = request.POST.get('stripeToken')
        amount = int(order.get_new_total * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='eur',
                source=token,
                description='Charge for {} (UID={})'.format(
                    request.user.email, request.user.id),
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id'][2:-3],
            payment.user = request.user
            payment.amount = order.get_new_total
            payment.save()

            order.ordered = True
            order.ordered_date = timezone.now()
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()
            if order.coupon is not None:
                order.coupon.used_by.add(request.user)

            for course in order.courses.all():
                course.students.add(request.user)
                messages.info(request, _(
                    f"Bienvenue au cours : {course.title}"))

            messages.success(request, _(
                "Votre commande a été affectué avec succès"))
            return redirect('courses:list')
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, _(f"{err.get('message')}"))
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, _("Rate limit error"))
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, _("Invalid parameters"))
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, _("Not authenticated"))
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, _("Network error"))
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, _(
                "Something went wrong. You were not charged. Please try again"))
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            current_site = get_current_site(request)
            subject = _("Stripe error")
            message = render_to_string('billing/payment_error.html', {
                'protocol': settings.PROTOCOL,
                'domain': current_site.domain,
                'error': e
            })
            msg = EmailMultiAlternatives(
                subject, message, "proglanglearn@gmail.com", to=[superuser.email for superuser in User.objects.filter(is_superuser=True)])
            msg.send()
            messages.error(request, _(
                f"A serious error occurred. We have been notified"))
            pass
        return redirect('main:billing:cart')

        # form = CheckoutForm(request.POST or None)
        # if form.is_valid():
        #     pass
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except:
            context = {**kwargs}
        context['navbar_search_form'] = self.form_navbar()
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first(
        ) if Order.objects.filter(user=self.request.user, ordered=False).exists() else None
        context['type'] = 'payment'
        context['coupon_form'] = CouponForm()
        return context


class CartView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'billing/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_search_form'] = self.form_navbar()
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first(
        ) if Order.objects.filter(user=self.request.user, ordered=False).exists() else None
        context['type'] = 'cart'
        context['coupon_form'] = CouponForm()
        return context


def add_to_cart(request, course):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if course in order.courses.all():
            messages.info(request, _(
                "Le cours que vous essayé d'ajouter se trouve déjà dans le panier"))
        else:
            order.courses.add(course)
            messages.success(request, _("Cours ajouté au panier"))
    else:
        order = Order.objects.create(user=request.user)
        order.courses.add(course)
    return redirect('main:billing:cart')


def remove_course_to_cart(request, slug):
    course = get_object_or_404(Course, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if course in order.courses.all():
            order.courses.remove(course)
            messages.success(request, _(
                "Le cours a bien été enlevé de votre panier"))
        else:
            messages.warning(request, _(
                "Le cours ne se trouve pas dans votre panier"))
        if order.courses.all().count() == 0 and order.coupon is not None:
            if order.coupon.deactivate_date < timezone.now():
                order.coupon.limited += 1
                order.coupon.save()
            order.coupon = None
            order.save()
    else:
        messages.info(request, _("Votre panier est actuellement vide"))
    return redirect('courses:detail', slug=course.slug)


def remove_coupon_to_cart(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.coupon is not None:
            order.coupon = None
            order.save()
            if coupon.deactivate_date < timezone.now():
                coupon.limited += 1
                coupon.save()
            messages.success(request, _(
                "Le code promotionnel a bien été retiré de votre panier"))
        else:
            messages.warning(request, _(
                "Le code promotionnel n'est pas lié à votre panier et ne peut être retiré"))
    else:
        messages.warning(request, _("Votre panier est vide"))
    return redirect('main:billing:cart')


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        if coupon.limited == 0 or coupon.deactivate_date < timezone.now():
            messages.error(request, _("Ce coupon n'est plus valide"))
            return None
    except ObjectDoesNotExist:
        messages.warning(request, _("Ce coupon n'existe pas"))
        return None
    return coupon


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, ordered=False)
                coupon = get_coupon(request, code)
                if coupon is not None or coupon.limited == 0 or coupon.deactivate_date > timezone.now():
                    if request.user not in coupon.used_by.all():
                        order.coupon = coupon
                        order.save()
                        coupon.limited -= 1
                        coupon.save()
                        messages.success(request, _(
                            f"Coupon {order.coupon.code} ajouté"))
                        return redirect('main:billing:checkout')
                    messages.error(request, _(
                        "Vous avez déjà utilisé ce coupon lors d'un précédent achat"))
                    return redirect('main:billing:cart')
                messages.error(request, _(
                    "Le coupon saisi n'existe pas ou n'est plus disponible"))
                return redirect('main:billing:cart')
            except ObjectDoesNotExist:
                messages.warning(request, _(
                    "Vous n'avez aucun cours dans votre panier"))
                return redirect("course:list")
    messages.error(request, _("Méthode d'ajout de coupon non acceptée"))
    return redirect('main:billing:cart')

# TODO : Redefine all view functions by class-based views
# Make a pdf file to download after payment


class RefundRequestView(LoginRequiredMixin, NavbarSearchMixin, View):
    template_name = 'billing/refund_request.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = RefundForm(request.POST or None)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            try:
                order = Order.objects.get(ref_code=ref_code)
                if Refund.objects.filter(order=order).count() == 0 and order.ordered_date + timezone.timedelta(days=30) > timezone.now():
                    order.refund_requested = True
                    order.save()

                    refund = Refund()
                    refund.order = order
                    refund.reason = message
                    refund.save()

                    messages.info(request, _("Votre demande a été envoyée"))
                    return redirect('main:index')
                if Refund.objects.filter(order=order, rejected=True).count() > 0:
                    messages.error(request, _(
                        "La demande de remboursement a été rejetée"))
                messages.error(request, _(
                    "La période de remboursement a expirée ou vous avez déjà envoyé une demande"))
                return redirect('main:billing:refund')
            except ObjectDoesNotExist:
                messages.warning(request, _(
                    "Le code de référence mentionné n'existe pas"))
                return redirect('main:billing:refund')

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['navbar_search_form'] = self.form_navbar()
        context['form'] = RefundForm()
        return context
