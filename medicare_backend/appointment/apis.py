from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppointmentSerializer
from .models import Appointment
from notification.models import Notification
from account.models import User

from notification.utils import create_notification


@api_view(['POST'])
def create_appointment(request):
    user = request.user
    
    check = Appointment.objects.filter(created_by = user).order_by('-created_at').first()

    if check and check.status != Appointment.DONE:

        return Response(
            {'error': 'You cannot create a new appointment until your current appointmemt is completed'}, status=status.HTTP_400_BAD_REQUEST
        )
    
    body = request.data.get('body')
    created_for = request.data.get('created_for')



    if not  body:

        return Response({'error':'Body is required'}, status= status.HTTP_400_BAD_REQUEST)
        
    appointment = Appointment.objects.create(
        created_by = user,
        body = body,
        created_for_id = created_for if created_for else None
    )

    
    admin = User.objects.get(email='oga@gmail.com')

    
    notification = create_notification(user,admin,Notification.APPOINTMENT)
                         

    serializer = AppointmentSerializer(appointment)


    return Response(serializer.data, status=status.HTTP_201_CREATED)


