
from django.urls import path, include

from .payment_methods.payments_stripe import urls
urlpatterns = [
   path("stripe/", include(urls))
]