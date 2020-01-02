from django import forms
from django.utils.translation import gettext_lazy as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class CheckoutForm(forms.Form):
    name_on_cc = forms.CharField(label=_(
        "Nom sur la carte"), widget=forms.TextInput(attrs={'placeholder': 'DOE JOHN'}))
    cc_num = forms.CharField(label=_("Numéro de carte bancaire"), min_length=16, max_length=19, widget=forms.TextInput(
        attrs={'placeholder': '4242 4242 4242 4242', 'data-mask': '0000 0000 0000 0000'}))
    cc_date = forms.CharField(label=_("Date d'expiration"), min_length=4, max_length=7, widget=forms.TextInput(
        attrs={'placeholder': 'MM / YY', 'data-mask': '00 / 00'}))
    cc_cvc = forms.CharField(label=_("CVV / CVC"), min_length=3, max_length=4, widget=forms.TextInput(
        attrs={'placeholder': '????', 'data-mask': '0000'}))
    save_info = forms.BooleanField(label=_(
        "Sauvegarder la carte pour une prochaine fois"), widget=forms.CheckboxInput(), required=False)
    recaptcha = ReCaptchaField()

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['cc_num'] = int(''.join(cleaned_data['cc_num'].split()))
        cleaned_data['cc_date'] = ''.join(cleaned_data['cc_date'].split())
        print(cleaned_data)
        return cleaned_data


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Entrez un code promotionnel')}))


class RefundForm(forms.Form):
    ref_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _("Code de référence")
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': _("Entrez votre message"),
        'rows': 4
    }))
