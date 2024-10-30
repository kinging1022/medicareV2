from rest_framework.decorators import api_view, authentication_classes , permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppointmentSerializer
from .models import Appointment


@api_view(['POST'])
def create_appointment(request):
    user = request.user
    body = request.data.get('body')
    created_for = request.data.get('created_for')

    if not  body:

        return Response({'error':'Body is required'}, status= status.HTTP_400_BAD_REQUEST)
    
    appointment = Appointment.objects.create(
        created_by = user,
        body = body,
        created_for_id = created_for if created_for else None
    )

    serializer = AppointmentSerializer(appointment)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def appointments(request):
    appointments = Appointment.objects.filter(status='sent')

    serializer = AppointmentSerializer(appointments, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def user_appointments(request):
    user = request.user
    appointments = Appointment.objects.filter(created_by = user)

    serializer = AppointmentSerializer(appointments, many=True)

    return Response(serializer.data)