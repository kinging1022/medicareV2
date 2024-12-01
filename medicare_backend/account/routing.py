from django.urls import re_path
from .consumers import UserConsumer, MedicationConsumer
websocket_urlpatterns = [
    re_path(r"ws/users/$", UserConsumer.as_asgi()),
    re_path(r"ws/medications/$", MedicationConsumer.as_asgi())
    
]

