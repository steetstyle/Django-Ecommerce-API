from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def test(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.username)
    return HttpResponse("yok")
