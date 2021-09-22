from .hooks import *
from rest_framework.authentication import SessionAuthentication

class UnsafeSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, *args, **kwargs):
        '''
        Bypass the CSRF checks altogether
        '''
        pass