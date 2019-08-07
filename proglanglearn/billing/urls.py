from django.urls import path

from .views import (
    CartView,
    PaymentView,
    RefundRequestView,
    RefundDetailView,
    AddCourseToCart,
    RemoveCourseFromCart,
    AddCouponToCart,
    RemoveCouponFromCart,
    PDFPaymentView,
)


app_name = 'billing'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', PaymentView.as_view(), name='checkout'),
    path('refund/', RefundRequestView.as_view(), name='refund'),
    path('refund/<int:id>/', RefundDetailView.as_view(), name='refund-detail'),
    path('add-course/<str:course_slug>/',
         AddCourseToCart.as_view(), name='add-course'),
    path('remove-course/<str:course_slug>/',
         RemoveCourseFromCart.as_view(), name='remove-course'),
    path('add-coupon/', AddCouponToCart.as_view(), name='add-coupon'),
    path('remove-coupon-from-cart/<id>/',
         RemoveCouponFromCart.as_view(), name='remove-coupon-from-cart'),
    path('pdf/<str:ref_code>/', PDFPaymentView.as_view(), name='pdf'),
]
