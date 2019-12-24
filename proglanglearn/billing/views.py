from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DetailView, RedirectView, View
from django.views.generic.base import TemplateView

import stripe

from courses.models import Course
from main.mixins import NavbarSearchMixin
from .templatetags.cart_template_tags import cart_item_count
from .forms import CheckoutForm, CouponForm, RefundForm
from .mixins import UserCanViewCheckout
from .models import Order, Coupon, Payment, Refund
from .utils import create_ref_code, get_coupon, RenderPDF


User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


class CartView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'billing/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first(
        ) if Order.objects.filter(user=self.request.user, ordered=False).exists() else None
        context['type'] = 'cart'
        context['coupon_form'] = CouponForm()
        return context


class PaymentView(LoginRequiredMixin, UserCanViewCheckout, NavbarSearchMixin, View):
    template_name = 'billing/payment.html'

    def get(self, request, *args, **kwargs):
        messages.info(request, _("Ceci est une version test de ce site. Veuillez utiliser les informations suivantes pour la carte bancaire : 4242424242424242 07/20 000"))
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
            payment.stripe_charge_id = charge['id'],
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
                    "Bienvenue au cours : %(course_title)s") % {'course_title': course.title})

            messages.success(request, _(
                "Votre commande a été effectuée avec succès"))
            return redirect('courses:list')
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, _("%(message_error)s") %
                           {'message_error': err.get('message')})
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
                subject, message, to=[superuser.email for superuser in User.objects.filter(is_superuser=True)])
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
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first(
        ) if Order.objects.filter(user=self.request.user, ordered=False).exists() else None
        context['type'] = 'payment'
        context['coupon_form'] = CouponForm()
        return context


class AddCourseToCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs.get('course_slug'))
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs.first()
            if course in order.courses.all():
                messages.info(request, _(
                    "Le cours que vous essayez d'ajouter se trouve déjà dans le panier"))
            else:
                order.courses.add(course)
                messages.success(request, _("Cours ajouté au panier"))
        else:
            order = Order.objects.create(user=request.user)
            order.courses.add(course)
        return redirect('main:billing:cart')


class RemoveCourseFromCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs.get('course_slug'))
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if request.user.is_authenticated:
            if order_qs.exists():
                order = order_qs.first()
                if course in order.courses.all():
                    order.courses.remove(course)
                    if request.is_ajax():
                        if order.courses.all().count() == 0 and order.coupon is not None:
                            if order.coupon.deactivate_date < timezone.now():
                                order.coupon.limited += 1
                                order.coupon.save()
                            order.coupon = None
                            order.save()
                        context = self.get_context_data(**kwargs)
                        html = render_to_string('billing/cart_element.html', context, request=request)
                        return JsonResponse({'html': html, 'cart_item_count': cart_item_count(request.user)})
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
        else:
            messages.warning(request, _("Vous n'êtes pas connecté actuellement. Veuillez vous connecter pour enlever le cours de votre panier s'il si trouve"))
        return redirect('courses:detail', slug=course.slug)

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first(
        ) if Order.objects.filter(user=self.request.user, ordered=False).exists() else None
        context['coupon_form'] = CouponForm()
        return context


class AddCouponToCart(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, ordered=False)
                coupon = get_coupon(request, code)
                if coupon is not None:
                    if request.user not in coupon.used_by.all():
                        order.coupon = coupon
                        order.save()
                        coupon.limited -= 1
                        coupon.save()
                        if request.is_ajax():
                            context = self.get_context_data(**kwargs)
                            html = render_to_string('billing/payment_items.html', context, request=request)
                            return JsonResponse({'html': html})
                        messages.info(request, _("Code promotionnel %(code)s ajouté") % {'code': coupon.code})
                        return redirect('main:billing:cart')
                    if request.is_ajax():
                        context = self.get_context_data(**kwargs)
                        context['error_msg'] = _("Vous avez déjà utilisé ce coupon lors d'un précédent achat")
                        html = render_to_string('billing/payment_items.html', context, request=request)
                        return JsonResponse({'html': html})
                    messages.warning(request, _("Vous avez déjà utilisé ce coupon lors d'un précédent achat"))
                    return redirect('main:billing:cart')
                if request.is_ajax():
                    context = self.get_context_data(**kwargs)
                    context['error_msg'] =  _("Le coupon saisi n'existe pas ou n'est plus disponible")
                    html = render_to_string('billing/payment_items.html', context, request=request)
                    return JsonResponse({'html': html})
                messages.warning(request, _("Le coupon saisi n'existe pas ou n'est plus disponible"))
                return redirect('main:billing:cart')
            except ObjectDoesNotExist:
                messages(request, _("Vous n'avez aucun cours dans votre panier"))
                return redirect('courses:list')
        if request.is_ajax():
            context['error_msg'] =  _("Méthode d'ajout de coupon non acceptée")
            html = render_to_string('billing/payment_items.html', context, request=request)
            return JsonResponse({'html': html})
        messages.error(request, _("Méthode d'ajout de coupon non acceptée"))
        return redirect('main:billing:cart')
    
    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first(
        ) if Order.objects.filter(user=self.request.user, ordered=False).exists() else None
        context['coupon_form'] = CouponForm()
        return context


class RemoveCouponFromCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        coupon = get_object_or_404(Coupon, id=kwargs.get('id'))
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs.first()
            if order.coupon is not None:
                order.coupon = None
                order.save()
                if coupon.deactivate_date < timezone.now():
                    coupon.limited += 1
                    coupon.save()
                if request.is_ajax():
                    context = self.get_context_data(**kwargs)
                    html = render_to_string('billing/payment_items.html', context, request=request)
                    return JsonResponse({'html': html})
            else:
                if request.is_ajax():
                    context = self.get_context_data(**kwargs)
                    context['remove_coupon_error'] = _("Le code promotionnel n'est pas lié à votre panier et ne peut être retiré")
                    html = render_to_string('billing/payment_items.html', context, request=request)
                    return JsonResponse({'html': html})
                messages.error(request, _("Le code promotionnel n'est pas lié à votre panier et ne peut être retiré"))
        else:
            messages.warning(request, _("Votre panier est vide"))
        return redirect('main:billing:cart')
    
    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first(
        ) if Order.objects.filter(user=self.request.user, ordered=False).exists() else None
        context['coupon_form'] = CouponForm()
        return context


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
                if Refund.objects.filter(order=order).count() == 0 and order.ordered_date + timezone.timedelta(days=14) > timezone.now():
                    order.refund_requested = True
                    order.save()

                    refund = Refund()
                    refund.order = order
                    refund.reason = message
                    refund.save()

                    messages.info(request, _("Votre demande a été envoyée"))
                    return redirect('main:analytics:orders')
                if Refund.objects.filter(order=order, rejected=True).count() > 0:
                    messages.error(request, _(
                        "La demande de remboursement a été rejetée"))
                    return redirect('main:analytics:orders')
                messages.error(request, _(
                    "La période de remboursement a expiré ou vous avez déjà envoyé une demande"))
                return redirect('main:analytics:orders')
            except ObjectDoesNotExist:
                messages.warning(request, _(
                    "Le code de référence mentionné n'existe pas"))
                return redirect('main:billing:refund')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RefundForm()
        return context


class RefundDetailView(LoginRequiredMixin, NavbarSearchMixin, DetailView):
    model = Refund

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class PDFPaymentView(LoginRequiredMixin, View):
    pdf_template_name = 'billing/pdf/confirmation_payment.html'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, user=request.user, ref_code=self.kwargs.get('ref_code'), ordered=True)
        params = {
            'order': order,
            'payment': order.payment,
            'stripe_charge': stripe.Charge.retrieve(order.payment.stripe_charge_id[2:-3]),
            'refund_url': reverse('main:billing:refund'),
        }
        return RenderPDF.render(self.pdf_template_name, params, f"{order.ref_code}")
