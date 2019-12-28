from modeltranslation.translator import register, TranslationOptions

from .models import Language, Tag, EmailAdminNotificationForUsers, IndexBanner


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('name', 'content')


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name', 'content')


@register(EmailAdminNotificationForUsers)
class EmailAdminNotificationForUsersTranslationOptions(TranslationOptions):
    fields = ('subject', 'body')


@register(IndexBanner)
class IndexBannerTranslationOptions(TranslationOptions):
    fields = ('content',)
