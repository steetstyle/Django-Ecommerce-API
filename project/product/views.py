from django.shortcuts import render
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

from core.permissions import MarketOwnerPermission
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import filters

class ProductViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for viewing and editing Products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = '__all__'

    def get_permissions(self):
        if self.action in ['update','partial_update','destroy','create']:
            self.permission_classes = [IsAuthenticated, MarketOwnerPermission]
        else :
            self.permission_classes = [AllowAny]
        return super(self.__class__, self).get_permissions()