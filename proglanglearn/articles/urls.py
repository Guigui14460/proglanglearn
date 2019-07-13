from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    ArticleFavoriteToggleRedirectView,
)

app_name = 'articles'

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('add/', ArticleCreateView.as_view(), name='create'),
    path('<str:article_slug>/', ArticleDetailView.as_view(), name='detail'),
    path('<str:article_slug>/update/',
         ArticleUpdateView.as_view(), name='update'),
    path('<str:article_slug>/delete/',
         ArticleDeleteView.as_view(), name='delete'),
    path('<str:article_slug>/favorite/',
         ArticleFavoriteToggleRedirectView.as_view(), name='article-favorite'),
]
