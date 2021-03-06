from django.urls import path
from . import views

urlpatterns = [
    path('pay', views.pay, name='pay'),
    path('payviamomo', views.payViaMomo, name='pay_via_momo'),
    path('payviacrypto', views.payViaCrypto, name='pay_via_crypto'),
    path('seemomopayment/<paymentId>', views.checkMoMoPaymentStatus, name='see_momo_payment'),
    path('payviapaypal', views.payViaPayPal, name='pay_via_paypal'),
    path('paypalsuccess', views.paypalReturnSuccess, name='paypal_success'),
    path('paypalerror', views.paypalReturnError, name='paypal_error')
]