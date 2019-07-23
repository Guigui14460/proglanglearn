from django.urls import path

from .quiz_views import (
    QuizDetailView,
)

app_name = 'quizzes'

urlpatterns = [
    path('<int:id>/', QuizDetailView.as_view(), name='detail'),
]
# TODO quiz templates and urls
# TODO poll templates and urls