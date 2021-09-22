
from django.urls import path, include

from .payment_methods.payments_stripe import urls
from.views import test
urlpatterns = [
   path("stripe/", include(urls)),
   path('test', test)
]