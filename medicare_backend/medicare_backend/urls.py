
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/', include('appointment.urls')),
    path('api/',include('consultations.urls')),
    path('api/', include('notification.urls'))
    
    
]
