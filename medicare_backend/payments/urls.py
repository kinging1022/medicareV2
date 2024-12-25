from django.urls import path

from . import apis
from . import views
from . import webhook

urlpatterns = [
   path('payment/credit-price/', apis.get_credit_price, name='get_price'),
   path('create-checkout-session/', apis.checkout, name='checkout'),
   path('payment-success/', views.success, name='payment_success'),
   path('payment-cancel/', views.cancel, name='payment_cancel'),
   path('payments/billing/', apis.get_transaction, name='get_transaction'),
   path('payments/usercredits/', apis.get_credits, name='get_credits'),
   path('webhook/', webhook.webhook, name='stripe-webhook'),
   
]
