from modeltranslation.translator import register, TranslationOptions

from .models import ProgType


@register(ProgType)
class ProgTypeTranslationOptions(TranslationOptions):
    fields = ('profession_type',)
