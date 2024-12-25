import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicare_backend.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from appointment.routing import websocket_urlpatterns as appointment_websocket_urlpatterns
from consultations.routing import websocket_urlpatterns as consultation_websocket_urlpatterns
from notification.routing import websocket_urlpatterns as notifications_websocket_urlpatterns
from .middleware import JwtAuthMiddlewareStack  # Import your custom middleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            appointment_websocket_urlpatterns +
            consultation_websocket_urlpatterns +
            notifications_websocket_urlpatterns
        )
    ),
})
