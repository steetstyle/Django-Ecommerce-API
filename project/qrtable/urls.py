from rest_framework import routers
from django.urls import include, path

from .views import QRTableViewSet

router = routers.SimpleRouter()
router.register('', QRTableViewSet)

urlpatterns = [
    path('', include(router.urls)),
]