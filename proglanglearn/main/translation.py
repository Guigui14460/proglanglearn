from modeltranslation.translator import register, TranslationOptions

from .models import Language, Tag, EmailAdminNotificationForUsers


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('name', 'content')


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name', 'content')


@register(EmailAdminNotificationForUsers)
class EmailAdminNotificationForUsersTranslationOptions(TranslationOptions):
    fields = ('subject', 'body')
