from django.urls import path

from . import apis

urlpatterns = [
   path('reminder/create/<uuid:id>/', apis.set_reminder, name='set_reminder'),
   path('reminder/<uuid:id>/delete/', apis.delete_reminder, name='delete_reminder')
   
   
]