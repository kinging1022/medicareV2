from rest_framework.decorators import api_view, authentication_classes , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import NotificationSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import Notification


@api_view(['POST'])
def read_notification(request,id):

    try:

        notification = Notification.objects.filter(created_for=request.user).get(pk=id)
    
    except Notification.DoesNotExist:
        
        return Response({'message':'notification does not exist'},status=status.HTTP_400_BAD_REQUEST)


    notification.is_read = True
    notification.save()

    serializer = NotificationSerializer(notification)

    return Response({'message':'notification has been marked as read',
                     'notification': serializer.data },
                    
                    status=status.HTTP_200_OK)



@api_view(['POST'])
def read_notifications(request):

    try:
        notifications = Notification.objects.filter(created_for=request.user)
    
        if not notifications.exists():

        
            return Response({'message':'no ntifications found'},status=status.HTTP_400_BAD_REQUEST)
    
        notifications.update(is_read=True)
        


        serializer = NotificationSerializer(notifications, many=True)

        return Response({'message':'notifications has been marked as read',
                     'notifications': serializer.data }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)