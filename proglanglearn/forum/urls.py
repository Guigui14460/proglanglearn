from django.urls import path

from .views import (
    SubjectListView,
    SubjectDetailView,
    SubjectFavoriteToggleRedirectView,
    SubjectAnswerLikeToggleRedirectView,
    SubjectBestAnswerToggleRedirectView,
    SubjectCreateView,
)


app_name = 'forum'

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject-list'),
    path('<int:id>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('<int:id>/favorite/', SubjectFavoriteToggleRedirectView.as_view(),
         name='subject-favorite'),
    path('<int:subject_id>/<int:answer_id>/like/',
         SubjectAnswerLikeToggleRedirectView.as_view(), name='subject-answer-like'),
    path('<int:subject_id>/<int:answer_id>/subject-best-answer/',
         SubjectBestAnswerToggleRedirectView.as_view(), name='subject-best-answer'),
    path('create/', SubjectCreateView.as_view(), name='subject-create'),
]
