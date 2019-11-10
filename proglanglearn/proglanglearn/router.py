from django.contrib.auth import get_user_model

from rest_framework import routers

from articles.api.views import ArticleViewSet
from analytics.api.views import UserExperienceJournalViewSet
from courses.api.views import CourseViewSet, TutorialViewSet
from main.api.views import LanguageViewSet, TagViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('journals', UserExperienceJournalViewSet)
router.register('articles', ArticleViewSet)
router.register('courses', CourseViewSet)
router.register('tutorials', TutorialViewSet)
router.register('languages', LanguageViewSet)
router.register('tags', TagViewSet)
