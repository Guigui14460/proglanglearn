from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import now, timedelta
from django.utils.translation import ugettext as _

from courses.models import Course


User = get_user_model()


class Coupon(models.Model):
    code = models.CharField(max_length=20, verbose_name=_("Nom"))
    discount_price = models.FloatField(verbose_name=_("Prix déduit"))
    limited = models.PositiveSmallIntegerField(default=100, verbose_name=_(
        "Nombre de personnes qui peuvent utiliser le code"))
    deactivate_date = models.DateTimeField(default=now(
    ) + timedelta(days=30), verbose_name=_("Date de désactivation du code"), null=True, blank=True)
    used_by = models.ManyToManyField(
        User, related_name='codes', verbose_name=_("Code utilisé par"), blank=True)

    def get_remove_coupon_to_cart_url(self):
        return reverse('main:billing:remove-coupon-to-cart', kwargs={'id': self.id})

    class Meta:
        verbose_name = _("coupon promotionnel")
        verbose_name_plural = _("coupons promotionnels")

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='orders', verbose_name=_("Utilisateur"))
    ref_code = models.CharField(
        max_length=20, verbose_name=_("Code de référence"))
    courses = models.ManyToManyField(Course, verbose_name=_("Cours choisis"))
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Code de promotion attaché"))
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Date de création de l'ordre d'achat"))
    ordered_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Date de la transaction"))
    ordered = models.BooleanField(default=False, verbose_name=_("Commandé"))
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,
                                null=True, blank=True, verbose_name=_("Paiement associé"))
    refund_requested = models.BooleanField(
        default=False, verbose_name=_("Demande de remboursement"))
    refund_granted = models.BooleanField(
        default=False, verbose_name=_("Demande de remboursement acceptée"))

    class Meta:
        verbose_name = _("commande")
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
        return round(total, 2)

    @property
    def get_old_total(self):
        total = 0
        for course in self.courses.all():
            total += float(course.old_price)
        if self.coupon is not None:
            total -= self.coupon.discount_price
        return round(total, 2)


class Payment(models.Model):
    stripe_charge_id = models.CharField(
        max_length=50, verbose_name=_("Identifiant de paiement Stripe"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name=_("Utilisateur"))
    amount = models.FloatField(verbose_name=_("Montant"))
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Date du paiement"))

    class Meta:
        verbose_name = _("paiement")

    def __str__(self):
        return self.stripe_charge_id


class Refund(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name=_("Commande"))
    reason = models.TextField(verbose_name=_("Raison"))
    refund_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_(
        "Identifiant de remboursement Stripe"))
    accepted = models.BooleanField(default=False, verbose_name=_("Accepté"))
    rejected = models.BooleanField(default=False, verbose_name=_("Rejeté"))

    class Meta:
        verbose_name = _("remboursement")

    def __str__(self):
        return f"{self.order.user.username}"
