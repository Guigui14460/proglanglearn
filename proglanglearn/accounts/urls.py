from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import (
    AccountView,
    PersonalInfo,
    ChangePassword,
    ProfileInfo,
    DangerZone,
    CustomLoginView,
    RegistrationView,
    AccountActivationSentView,
    ActivateView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('signup/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('account/handle-personal-info/',
         PersonalInfo.as_view(), name='handle-personal-info'),
    path('account/handle-change-password/',
         ChangePassword.as_view(), name="handle-change-password"),
    path('account/handle-profile-info/',
         ProfileInfo.as_view(), name='handle-profile-info'),
    path('account/handle-danger-zone/',
         DangerZone.as_view(), name='handle-danger-zone'),
    path('account-activation-sent/',
         AccountActivationSentView.as_view(), name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('password-reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
