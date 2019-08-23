from modeltranslation.translator import register, TranslationOptions

from .models import Poll, Item


@register(Poll)
class PollTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ('value',)
