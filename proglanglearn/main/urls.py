from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    IndexView,
    AboutView,
    CommentReportView,
    CommentDeleteView,
    ContactView,
    PrivacyView,
    PrivacyModalView,
    TermsView,
    SearchView,
    LanguagesTagsView,
)

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('search/', SearchView.as_view(), name='search'),
    path('report/<int:comment_id>/',
         CommentReportView.as_view(), name='report-comment'),
    path('delete/<int:comment_id>/',
         CommentDeleteView.as_view(), name='delete-comment'),
    path('tags/<str:slug>/', LanguagesTagsView.as_view(), name='language_tag'),
    path('', include('analytics.urls')),
    path('payment/', include('billing.urls')),
    path('robots.txt', TemplateView.as_view(
        template_name="main/robots.txt", content_type="text/plain")),
    path('modal-privacy/', PrivacyModalView.as_view()),
]
