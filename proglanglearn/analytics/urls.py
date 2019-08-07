from django.urls import path

from .views import (
    DashboardView,
    FavoriteArticleView,
    FavoriteTutorialView,
    OrderListView,
    MyCommentReportListView,
    MyCoursesListView,
)


app_name = 'analytics'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('favorite-articles/', FavoriteArticleView.as_view(),
         name='favorite-articles'),
    path('favorite-tutorials/', FavoriteTutorialView.as_view(),
         name='favorite-tutorials'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('comment-report/', MyCommentReportListView.as_view(), name='comment-report'),
    path('my-courses/', MyCoursesListView.as_view(), name='my-courses'),
]
