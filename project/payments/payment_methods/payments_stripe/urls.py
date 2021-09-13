
from django.urls import path, include
from .views import custom_webhook

urlpatterns = [
   path("", include("djstripe.urls", namespace="djstripe")),
   path("custom_webhook", custom_webhook)
]