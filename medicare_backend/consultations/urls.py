from django.urls import path

from . import apis

urlpatterns = [
   path('consultation/create/<uuid:id>/',apis.create_consultation,name='create_consultation'),
   path('consultation/sessions/create/<uuid:consultation_id>/<uuid:patient_id>/',apis.get_or_create_doctor_session,name='create_session'),
   path('consultation/sessions/medications/<uuid:id>/', apis.add_medications, name='add_medication')

     
]
