from django.urls import path

from . import apis

urlpatterns = [
   path('consultation/create/<uuid:id>/',apis.create_consultation,name='create_consultation'),
   path('consultation/sessions/create/<uuid:id>/',apis.get_or_create_doctor_session,name='create_session'),
   path('consultation/sessions/message/<uuid:id>/',apis.session_send_message,name='session_send_message'),

     
]
