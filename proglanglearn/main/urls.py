from django.urls import path

from .views import (
    IndexView,
    AboutView,
    ContactView,
    PrivacyView,
    TermsView,
    SearchView,
)

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('search/', SearchView.as_view(), name='search'),
]
