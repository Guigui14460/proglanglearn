from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from .views import (
    CustomLoginView,
    RegistrationView,
    AccountActivationSentView,
    activate,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('signup/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account-activation-sent/',
         AccountActivationSentView.as_view(), name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password-reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
