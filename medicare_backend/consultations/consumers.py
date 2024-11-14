from channels.db import database_sync_to_async
import json
import uuid
from django.core.serializers.json import DjangoJSONEncoder
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin, action
from account.models import User
from account.serializers import UserSerializer
from djangochannelsrestframework.permissions import IsAuthenticated 


from .models import Consultation
from .serializers import ConsultationSerializer, DoctorSession, DoctorSessionMessage
from .serializers import SessionMessageSerializer ,SessionDetailSerializer , SessionSerializer

class ConsultationConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = (permissions.AllowAny,)  # Note the trailing comma
    

    async def connect(self):
        await self.model_change.subscribe()  # Ensure model_change is defined
        await super().connect()

    @model_observer(Consultation)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data=ConsultationSerializer(instance=instance).data, action=action.value)
    



class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

    

class DoctorSessionConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = DoctorSession.objects.all()
    serializer_class = SessionDetailSerializer
    lookup_field = "pk"

    async def send_json(self, content, close=False):
        # Use CustomJSONEncoder for UUID handling
        await super().send(text_data=json.dumps(content, cls=CustomJSONEncoder), close=close)


 

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message, **kwargs):
        room: DoctorSession = await self.get_room(pk=self.room_subscribe)
        await database_sync_to_async(DoctorSessionMessage.objects.create)(
            doctor_session=room,
            created_by=self.scope["user"],
            body=message
        )

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @model_observer(DoctorSessionMessage)
    async def message_activity(self, message, observer=None, **kwargs):
    
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: DoctorSessionMessage, **kwargs):
        yield f'room__{instance.doctor_session.id}'
        yield f'pk__{instance.doctor_session.id}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance: DoctorSessionMessage, action, **kwargs):
        data = SessionMessageSerializer(instance).data
        data['pk'] = str(instance.pk)
        return dict(data=data, action=action.value)

    async def notify_users(self):
        room: DoctorSession = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> DoctorSession:
        return DoctorSession.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, room: DoctorSession):
        return [UserSerializer(user).data for user in room.users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user: User = self.scope["user"]
        user.doctor_session.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user = self.scope["user"]
        # Check if the user is authenticated
        if user.is_authenticated:
            # Only add the user if they are not already in the room
            if not user.doctor_session.filter(pk=self.room_subscribe).exists():
                user.doctor_session.add(DoctorSession.objects.get(pk=pk))
        else:
            print("User is not authenticated. Cannot add to room.")



