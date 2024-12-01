from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from asgiref.sync import sync_to_async


from .models import Notification
from .serializers import NotificationSerializer


class NotificationConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def filter_queryset(self, queryset, **kwargs):
        
        user = self.scope['user']

        
        return queryset.filter(created_for=user)  

    async def connect(self):
        # Establish subscription to model changes
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Notification)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        # Serialize instance and include the action
        return dict(data=NotificationSerializer(instance=instance).data, action=action.value)