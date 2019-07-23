from django.urls import path

from .views import (
    PaymentView,
)


app_name = 'billing'

urlpatterns = [
    path('checkout/', PaymentView.as_view(), name='checkout'),
]
