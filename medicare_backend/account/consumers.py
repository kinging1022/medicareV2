from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from consultations.models import Medications
from consultations.serializers import MedicationsSerializer
from .models import User
from .serializers import UserSerializer
import json
import uuid
from django.core.serializers.json import DjangoJSONEncoder

class UserConsumer(ListModelMixin,GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def filter_queryset(self, queryset, **kwargs):
        
        return queryset.filter(role=User.DOCTOR)  # Filter appointments for patients



    async def connect(self):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(User)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data=UserSerializer(instance=instance).data, action=action.value)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


class MedicationConsumer(ListModelMixin,GenericAsyncAPIConsumer):
    queryset = Medications.objects.all()
    serializer_class = MedicationsSerializer

    async def send_json(self, content, close=False):
        # Use CustomJSONEncoder for UUID handling
        await super().send(text_data=json.dumps(content, cls=CustomJSONEncoder), close=close)


    
    def filter_queryset(self, queryset, **kwargs):
        user = self.scope['user']
        return queryset.filter(created_for=user)
    

    async def connect(self):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Medications)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data=MedicationsSerializer(instance=instance).data, action=action.value)




