from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import QRTable
from .serializers import QRTableSerializer

from core.permissions import MarketOwnerPermission
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import filters

class CSRFExemptModelViewSet(viewsets.ModelViewSet):

    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        return super(CSRFExemptModelViewSet, self).create(request, *args, **kwargs)
    
    @method_decorator(csrf_exempt)
    def list(self, request, *args, **kwargs):
        return super(CSRFExemptModelViewSet, self).list(request, *args, **kwargs)
    
    @method_decorator(csrf_exempt)
    def retrieve(self, request, *args, **kwargs):
        return super(CSRFExemptModelViewSet, self).retrieve(request, *args, **kwargs)
    
    @method_decorator(csrf_exempt)
    def update(self, request, *args, **kwargs):
        return super(CSRFExemptModelViewSet, self).update(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def destroy(self, request, *args, **kwargs):
        return super(CSRFExemptModelViewSet, self).destroy(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFExemptModelViewSet, self).dispatch(request, *args, **kwargs)

class QRTableViewSet(CSRFExemptModelViewSet):
    """
    A ModelViewSet for viewing and editing QRTables.
    """
    queryset = QRTable.objects.all()
    serializer_class = QRTableSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['code']

    def get_permissions(self):
        if self.action in ['update','partial_update','destroy','create']:
            self.permission_classes = [IsAuthenticated, MarketOwnerPermission]
        else :
            self.permission_classes = [AllowAny]
        return super(self.__class__, self).get_permissions()

