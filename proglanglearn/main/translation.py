from modeltranslation.translator import register, TranslationOptions

from .models import Language, Tag


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('name', 'content')


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name', 'content')
