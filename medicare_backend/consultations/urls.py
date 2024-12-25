from django.urls import path

from . import apis

urlpatterns = [
   path('consultation/<uuid:id>/', apis.view_session, name='view_session'),
   path('consultation/session-history/', apis.session_history, name='session_history'),
   path('consultation/active-session/', apis.get_active_session, name='active_session'),
   path('consultation/sessions/end/<uuid:id>/', apis.end_session, name='end_session'),
   path('consultation/create/<uuid:id>/',apis.create_consultation,name='create_consultation'),
   path('consultation/sessions/create/<uuid:consultation_id>/<uuid:patient_id>/',apis.get_or_create_doctor_session,name='create_session'),
   path('consultation/sessions/medications/<uuid:id>/', apis.add_medications, name='add_medication'),
   path('consultation/session/message/<uuid:id>/',apis.send_message, name='send_message'),
     
]

