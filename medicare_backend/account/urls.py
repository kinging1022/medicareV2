from django.urls import path, include
from djoser import views as djoser_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import apis

urlpatterns = [
    # Uncomment the following paths if you want to use custom user views
    # path('auth/users/', djoser_views.UserViewSet.as_view({'post': 'create'}), name='user-create'),
    # path('auth/users/<uuid:pk>/', djoser_views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    # path('auth/users/me/', djoser_views.UserViewSet.as_view({'get': 'me'}), name='user-me'),

    # Custom JWT views for login, refresh, and verify
    path('auth/token/login/', TokenObtainPairView.as_view(), name='token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('update/<uuid:id>/', apis.update_profile, name='update_profile'),
    
    # Djoser URLs
    path('auth/', include('djoser.urls')),
    path('doctors/', apis.doctors, name='doctors')
     
]