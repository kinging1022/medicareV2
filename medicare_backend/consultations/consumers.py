import json
import uuid
from typing import Dict, Any
from uuid import UUID
from djangochannelsrestframework import permissions
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.permissions import IsAuthenticated
from .models import Consultation, DoctorSession, DoctorSessionMessage
from .serializers import (
    SessionDetailSerializer,
    ConsultationSerializer,
    SessionMessageSerializer,
    SessionSerializer
)
from account.models import User
from account.serializers import UserSerializer





class CustomJSONEncoder(json.JSONEncoder):
    

    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)
    




class DoctorSessionConsumer(ListModelMixin, GenericAsyncAPIConsumer):
   queryset = DoctorSession.objects.all()
   serializer_class = SessionDetailSerializer
   permission_classes = (permissions.IsAuthenticated,)



   async def send_json(self, content, close=False):
    await super().send(text_data=json.dumps(content, cls=CustomJSONEncoder), close=close)
       
   
   
   def filter_queryset(self, queryset, **kwargs):
       user = self.scope["user"]
       status = kwargs.get("status", DoctorSession.STARTED)
       return queryset.filter(users=user, status=status)

   async def connect(self):
       await self.model_change.subscribe()
       await super().connect()

   @model_observer(DoctorSessionMessage)
   async def model_change(self, message, observer=None, **kwargs):
       await self.send_json(message)

   @model_change.serializer
   def model_serializer(self, instance, action, **kwargs):
       data = SessionMessageSerializer(instance=instance).data
       return dict(data=data, action=action.value)
    
   
    


class ConsultationConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


    

    def filter_queryset(self, queryset, **kwargs):
        
        user = self.scope["user"]
        return queryset.filter(created_for=user)

    async def connect(self):
        
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Consultation)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        data = ConsultationSerializer(instance=instance).data
        return dict(data=data, action=action.value)
    

