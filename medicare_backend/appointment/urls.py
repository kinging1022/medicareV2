from django.urls import path

from . import apis

urlpatterns = [
   path('request/appointment/', apis.create_appointment, name='request_appointment'),
   path('appointments/', apis.appointments, name='appointments'),
   path('user/appointments/', apis.user_appointments, name='user_appointments')
     
]