from django.urls import path, include
from django.conf import settings

from project.producer.views import send

urlpatterns = [
    path('send/<username>/<data>/<token>', send, name='send_message'),
]

