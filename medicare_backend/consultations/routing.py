from django.urls import re_path
from .consumers import ConsultationConsumer , DoctorSessionConsumer

websocket_urlpatterns = [
    re_path(r"ws/consultations/$", ConsultationConsumer.as_asgi()),
    re_path(r'ws/session-chat/$', DoctorSessionConsumer.as_asgi()),
]

