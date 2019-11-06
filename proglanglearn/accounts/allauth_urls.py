from django.urls import path, include

from .allauth_views import *


urlpatterns = [
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('password/change/', PasswordChangeView.as_view(),
         name='account_change_password'),
    path('password/set/', PasswordSetView.as_view(), name='account_set_password'),
    path('inactive/', AccountInactiveView.as_view(), name='account_inactive'),
    path('email/', EmailView.as_view(), name='account_email'),
    path('confirm-email/', EmailVerificationSentView.as_view(),
         name='account_email_verification_sent'),
    #     path('confirm-email/<str:key>/', ConfirmEmailView.as_view(),
    #          name='account_confirm_email'),
    path('password/reset/', PasswordResetView.as_view(),
         name='account_reset_password'),
    path('password/reset/done/', PasswordResetDoneView.as_view(),
         name='account_reset_password_done'),
    path('password/reset/key/<str:uidb36>-<str:key>/',
         PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/key/done/', PasswordResetFromKeyDoneView.as_view(),
         name='account_reset_password_from_key_done'),
    path('', include('allauth.urls')),
]
