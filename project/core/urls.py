# Django 2.0+
from django.urls import path
import django_cas_ng.views

urlpatterns = [
    # ...
    path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
]