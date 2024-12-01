from django.urls import path

from . import apis

urlpatterns = [
   path('notifications/read/<uuid:id>/',apis.read_notification,name='read_notification'),
   path('notifications/read/',apis.read_notifications,name='read_notifications'),
      
]