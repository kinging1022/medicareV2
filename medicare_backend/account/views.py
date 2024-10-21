from django.shortcuts import render
from .models import User

# Create your views here.

def activate_user(request):

    uid = request.GET.get('uid')
    token = request.GET.get('token')

    if uid and token:
        user = User.objects.get(id=uid)

        user.is_active = True
        user.save()
