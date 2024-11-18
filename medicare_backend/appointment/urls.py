from django.urls import path

from . import apis

urlpatterns = [
   path('request/appointment/', apis.create_appointment, name='request_appointment'),
   
]