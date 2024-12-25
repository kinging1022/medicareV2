from django.urls import path, include
from djoser import views as djoser_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .apis import CustomTokenObtainPairView, update_profile , update_timezone, get_doctors, get_medications

urlpatterns = [
    # Custom JWT views for login, refresh, and verify
    path('auth/token/login/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('update/<uuid:id>/', update_profile, name='update_profile'),
    path('user/update-timezone/', update_timezone, name='update_timezone'),
    path('account/medications/', get_medications, name='get_medications'),
    path('account/get_doctors/', get_doctors, name='get_doctors'),
    
    # Djoser URLs
    path('auth/', include('djoser.urls')),
    
     
]

