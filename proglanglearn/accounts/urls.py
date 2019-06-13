from django.urls import path

from .views import (
    index,
    about,
    privacy,
    terms,
    contact
)

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('privacy/', privacy, name='privacy'),
    path('about/', about, name='about'),
    path('terms/', terms, name='terms'),
]
