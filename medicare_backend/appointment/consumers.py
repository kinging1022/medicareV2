from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from asgiref.sync import sync_to_async

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = (permissions.AllowAny,)  # Uncomment if needed

    def filter_queryset(self, queryset, **kwargs):
        """
        Return all appointments for admin users and filtered appointments for patients.
        """
        user = self.scope['user']

        if user.is_staff:  # Check if the user is an admin
            return queryset  # Return all appointments for admin
        else:
            return queryset.filter(created_by=user)  # Filter appointments for patients

    async def connect(self):
        # Establish subscription to model changes
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Appointment)
    async def model_change(self, message, observer=None, **kwargs):
        # Send JSON message to WebSocket
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        # Serialize instance and include the action
        return dict(data=AppointmentSerializer(instance=instance).data, action=action.value)



