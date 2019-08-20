from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _

from courses.models import Course


User = get_user_model()


class Coupon(models.Model):
    code = models.CharField(max_length=20, verbose_name=_("nom"))
    discount_price = models.FloatField(verbose_name=_("prix déduit"))
    limited = models.PositiveSmallIntegerField(default=100, verbose_name=_(
        "nombre de personnes qui peuvent utiliser le code"))
    deactivate_date = models.DateTimeField(auto_now_add=True, verbose_name=_("date de désactivation du code"), null=True, blank=True)
    used_by = models.ManyToManyField(
        User, related_name='codes', verbose_name=_("code utilisé par"), blank=True)

    def get_remove_coupon_from_cart_url(self):
        return reverse('main:billing:remove-coupon-from-cart', kwargs={'id': self.id})

    class Meta:
        verbose_name = _("coupon promotionnel")
        verbose_name_plural = _("coupons promotionnels")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        d = timedelta(days=30)
        if not self.id:
            super(Coupon, self).save(*args, **kwargs)
            self.deactivate_date += d
            super(Coupon, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='orders', verbose_name=_("utilisateur"))
    ref_code = models.CharField(
        max_length=20, verbose_name=_("code de référence"))
    courses = models.ManyToManyField(Course, verbose_name=_("cours choisis"))
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("code de promotion attaché"))
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date de création de l'ordre d'achat"))
    ordered_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("date de la transaction"))
    ordered = models.BooleanField(default=False, verbose_name=_("commandé"))
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,
                                null=True, blank=True, verbose_name=_("paiement associé"))
    refund_requested = models.BooleanField(
        default=False, verbose_name=_("demande de remboursement"))
    refund_granted = models.BooleanField(
        default=False, verbose_name=_("demande de remboursement acceptée"))

    class Meta:
        verbose_name = _("commande")
        verbose_name_plural = _("commandes")
        ordering = ['-ordered_date', '-start_date']

    def __str__(self):
        return f"{self.user.username} - {self.start_date}"

    @property
    def get_new_total(self):
        total = 0
        for course in self.courses.all():
            if course.new_price is not None:
                total += float(course.new_price)
            else:
                total += float(course.old_price)
        if self.coupon is not None:
            total -= self.coupon.discount_price
        final_total = round(total, 2)
        if total > 0:
            return final_total
        else:
            return 0

    @property
    def get_old_total(self):
        total = 0
        for course in self.courses.all():
            total += float(course.old_price)
        if self.coupon is not None:
            total -= self.coupon.discount_price
        final_total = round(total, 2)
        if total > 0:
            return final_total
        else:
            return 0

    def get_refund(self):
        try:
            return Refund.objects.get(order=self)
        except:
            return Refund.objects.none()

    def render_pdf(self):
        return reverse('main:billing:pdf', kwargs={'ref_code': self.ref_code})


class Payment(models.Model):
    stripe_charge_id = models.CharField(
        max_length=50, verbose_name=_("identifiant de paiement Stripe"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name=_("utilisateur"))
    amount = models.FloatField(verbose_name=_("montant"))
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date du paiement"))

    class Meta:
        verbose_name = _("paiement")
        verbose_name_plural = _("paiements")

    def __str__(self):
        return self.stripe_charge_id


class Refund(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name=_("commande"))
    reason = models.TextField(verbose_name=_("raison"))
    refund_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_(
        "identifiant de remboursement Stripe"))
    accepted = models.BooleanField(default=False, verbose_name=_("accepté"))
    rejected = models.BooleanField(default=False, verbose_name=_("rejeté"))

    class Meta:
        verbose_name = _("remboursement")
        verbose_name_plural = _("remboursements")
        ordering = ['-id']

    def __str__(self):
        return f"{self.order.user.username}"

    def get_absolute_url(self):
        return reverse('main:billing:refund-detail', kwargs={'id': self.id})
