from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/', include('appointment.urls')),
    path('api/',include('consultations.urls')),
    path('api/', include('notification.urls')),
    path('api/', include('reminder.urls')),
    path('', include('payments.urls'))
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


