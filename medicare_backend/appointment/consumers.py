import json
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer



from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = (permissions.AllowAny,)  # Note the trailing comma
    

    async def connect(self):
        await self.model_change.subscribe()  # Ensure model_change is defined
        await super().connect()

    @model_observer(Appointment)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data=AppointmentSerializer(instance=instance).data, action=action.value)

