from django.urls import path

from .views import (
    CourseCreateView,
    CourseDeleteView,
    CourseDetailView,
    CourseListView,
    CourseUpdateView,
    CourseUserEnrolledView,
    TutorialCreateView,
    TutorialDetailView,
    TutorialFavoriteToggleRedirectView,
    TutorialUpdateView,
    TutorialDeleteView
)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('add/', CourseCreateView.as_view(), name='create'),
    path('<str:slug>/', CourseDetailView.as_view(), name='detail'),
    path('<str:slug>/user-enrolling/',
         CourseUserEnrolledView.as_view(), name='user-enrolling'),
    path('<str:slug>/update/', CourseUpdateView.as_view(), name='update'),
    path('<str:slug>/delete/', CourseDeleteView.as_view(), name='delete'),
    path('<str:course_slug>/add/',
         TutorialCreateView.as_view(), name='tutorial-create'),
    path('<str:course_slug>/<str:tutorial_slug>/',
         TutorialDetailView.as_view(), name='tutorial-detail'),
    path('<str:course_slug>/<str:slug>/update/',
         TutorialUpdateView.as_view(), name='tutorial-update'),
    path('<str:course_slug>/<str:tutorial_slug>/delete/',
         TutorialDeleteView.as_view(), name='tutorial-delete'),
    path('<str:course_slug>/<str:tutorial_slug>/favorite/',
         TutorialFavoriteToggleRedirectView.as_view(), name='tutorial-favorite'),
]
