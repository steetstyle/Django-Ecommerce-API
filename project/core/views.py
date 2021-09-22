from rest_framework import viewsets
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .serializers import AuthProfileDetailSerializer

UserModel = get_user_model()

class AuthProfileDetail(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        user = request.user
        print(user)
        serializer = AuthProfileDetailSerializer(user, context={'request':request})
        return Response(serializer.data)