from modeltranslation.translator import register, TranslationOptions

from .models import Course, Tutorial


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'content_introduction')


@register(Tutorial)
class TutorialTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
