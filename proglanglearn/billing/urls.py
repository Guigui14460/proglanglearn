from django.urls import path

from .views import (
    CartView,
    PaymentView,
    RefundRequestView,
    add_coupon,
    remove_coupon_to_cart,
    remove_course_to_cart,
)


app_name = 'billing'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', PaymentView.as_view(), name='checkout'),
    path('refund/', RefundRequestView.as_view(), name='refund'),
    path('add-coupon/', add_coupon, name='add-coupon'),
    path('remove-coupon-to-cart/<id>/',
         remove_coupon_to_cart, name='remove-coupon-to-cart'),
    path('remove-course-to-cart/<slug>/',
         remove_course_to_cart, name='remove-course-to-cart'),
]
