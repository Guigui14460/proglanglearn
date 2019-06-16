from django.urls import path

from .views import (
    IndexView,
    about,
    contact,
    privacy,
    terms,
    search,
)

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('privacy/', privacy, name='privacy'),
    path('terms/', terms, name='terms'),
    path('search/', search, name='search'),
]
