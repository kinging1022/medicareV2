from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import User
from .serializers import UserSerializer

class UserConsumer(ListModelMixin,GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


    async def connect(self):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(User)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data=UserSerializer(instance=instance).data, action=action.value)
