from django.conf import settings
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin
import stripe

from .models import Order, Payment, Coupon, Refund


stripe.api_key = settings.STRIPE_SECRET_KEY


def make_refund_accepted(model_admin, request, queryset):
    try:
        for refund in queryset:
            refund.order.refund_requested = True
            refund.order.refund_granted = True
            refund.order.save()
            charge_id = refund.order.payment.stripe_charge_id[2:-3]
            refund_object = stripe.Refund.create(
                charge=charge_id,
                amount=int(refund.order.payment.amount * 95),
            )
            refund.refund_id = refund_object['id']
            refund.accepted = True
            refund.save()

            for course in refund.order.courses.all():
                course.students.remove(refund.order.user)
        messages.success(request, _(
            "Remboursements effectués"))
    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get('error', {})
        messages.error(request, _("%(error)s") % {'error': err.get('message')})
    except stripe.error.RateLimitError as e:
        messages.error(request, _("Rate limit error"))
    except stripe.error.InvalidRequestError as e:
        messages.error(request, _("Invalid parameters"))
    except stripe.error.AuthenticationError as e:
        messages.error(request, _("Not authenticated"))
    except stripe.error.APIConnectionError as e:
        messages.error(request, _("Network error"))
    except stripe.error.StripeError as e:
        messages.error(request, _(
            "Something went wrong. You were not charged. Please try again"))
    except Exception as e:
        messages.error(request, str(e))


make_refund_accepted.short_description = _(
    "Mise des commandes vers l'acceptation du remboursement")


def make_refund_rejected(model_admin, request, queryset):
    for refund in queryset:
        refund.order.refund_requested = True
        refund.order.refund_granted = False
        refund.order.save()
        refund.rejected = True
        refund.save()
    messages.success(request, _(
        "Remboursements rejetés avec succès"))


make_refund_rejected.short_description = _(
    "Rejet de la demande de remboursement")


class CouponAdmin(ImportExportModelAdmin):
    list_display = ('code', 'discount_price', 'limited', 'deactivate_date')
    search_fields = ['code']


class OrderAdmin(ImportExportModelAdmin):
    list_display = ('user', 'ordered_date', 'start_date',
                    'get_payment_link', 'refund_requested', 'refund_granted')
    search_fields = ['user__username', 'payment__stripe_charge_id', 'ref_code']
    list_filter = ['start_date', 'ordered_date',
                   'refund_requested', 'refund_granted']
    empty_value_display = _("Pas encore commandé")

    def get_payment_link(self, obj=None):
        if obj.pk:
            if obj.payment is None:
                return _("Pas encore commandé")
            return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(obj.payment._meta.app_label, obj.payment._meta.model_name), args=(obj.payment.pk,))}'>{obj.payment.stripe_charge_id}</a>")
        return _("Enregistrez un paiement pour avoir le lien")
    get_payment_link.allow_tags = True
    get_payment_link.short_description = _("Lien du paiement")


class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('stripe_charge_id', 'get_user_link', 'amount', 'timestamp')
    search_fields = ['user__username', 'stripe_charge_id']
    list_filter = ['timestamp']

    def get_user_link(self, obj=None):
        if obj.pk:
            try:
                return mark_safe(f"<a href='{reverse('admin:{}_{}_change'.format(obj.user._meta.app_label, obj.user._meta.model_name), args=(obj.user.pk,))}'>{obj.user.username}</a>")
            except:
                return _("Utilisateur supprimé")
        return _("Enregistrez un paiement pour avoir le lien")
    get_user_link.allow_tags = True
    get_user_link.short_description = _("Lien de l'utilisateur")


class RefundAdmin(ImportExportModelAdmin):
    list_display = ('order', 'refund_id', 'accepted', 'rejected')
    empty_value_display = _("Remboursement non acceptée")
    search_fields = ['order__ref_code', 'order__user__username', 'refund_id']
    list_filter = ['accepted', 'rejected']
    actions = [make_refund_accepted, make_refund_rejected]


admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Refund, RefundAdmin)
