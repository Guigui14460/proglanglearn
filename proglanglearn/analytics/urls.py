from django.urls import path

from .views import (
    DashboardView,
    RankingView,
    FavoriteArticleView,
    FavoriteTutorialView,
    FavoriteSubjectView,
    OrderListView,
    MyCommentReportListView,
    MyCoursesListView,
    MyArticlesListView,
    MySubjectsListView,
)


app_name = 'analytics'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('favorite-articles/', FavoriteArticleView.as_view(),
         name='favorite-articles'),
    path('favorite-tutorials/', FavoriteTutorialView.as_view(),
         name='favorite-tutorials'),
    path('favorite-subjects/', FavoriteSubjectView.as_view(),
         name='favorite-subjects'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('comment-report/', MyCommentReportListView.as_view(), name='comment-report'),
    path('my-courses/', MyCoursesListView.as_view(), name='my-courses'),
    path('my-articles/', MyArticlesListView.as_view(), name='my-articles'),
    path('my-subjects/', MySubjectsListView.as_view(), name='my-subjects'),
]
