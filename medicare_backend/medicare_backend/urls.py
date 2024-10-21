
from django.contrib import admin
from django.urls import path, include
from account.views import activate_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
     path('auth/activate/', activate_user, name='activate_user' ),
    
]
