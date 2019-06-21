from django.urls import path

from .views import (
    CourseCreateView,
    CourseDeleteView,
    CourseDetailView,
    CourseListView,
    CourseUpdateView,
)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('add/', CourseCreateView.as_view(), name='create'),
    path('<int:id>/', CourseDetailView.as_view(), name='detail'),
    path('<int:id>/update/', CourseUpdateView.as_view(), name='update'),
    path('<int:id>/delete/', CourseDeleteView.as_view(), name='delete'),
]
