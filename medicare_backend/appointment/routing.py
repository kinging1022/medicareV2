from django.urls import re_path
from .consumers import AppointmentConsumer

websocket_urlpatterns = [
    #re_path(r"ws/patient/appointments/$", PatientAppointmentConsumer.as_asgi()),
    re_path(r"ws/appointments/$", AppointmentConsumer.as_asgi()),
]
