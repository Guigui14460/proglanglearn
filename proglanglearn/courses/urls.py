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
)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('add/', CourseCreateView.as_view(), name='create'),
    path('<int:id>/', CourseDetailView.as_view(), name='detail'),
    path('<int:id>/user-enrolling/',
         CourseUserEnrolledView.as_view(), name='user-enrolling'),
    path('<int:id>/update/', CourseUpdateView.as_view(), name='update'),
    path('<int:id>/delete/', CourseDeleteView.as_view(), name='delete'),
    path('<int:course_id>/add/',
         TutorialCreateView.as_view(), name='tutorial-create'),
    path('<int:course_id>/<int:tutorial_id>/',
         TutorialDetailView.as_view(), name='tutorial-detail'),
    path('<int:course_id>/<int:tutorial_id>/update/',
         TutorialDetailView.as_view(), name='tutorial-update'),
    path('<int:course_id>/<int:tutorial_id>/delete/',
         TutorialDetailView.as_view(), name='tutorial-delete'),
    path('<int:course_id>/<int:tutorial_id>/favorite/',
         TutorialFavoriteToggleRedirectView.as_view(), name='tutorial-favorite'),
]
