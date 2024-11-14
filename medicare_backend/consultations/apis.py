from rest_framework.decorators import api_view, authentication_classes , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ConsultationSerializer , SessionDetailSerializer, SessionMessageSerializer, SessionSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import Consultation , DoctorSession, DoctorSessionMessage
from account.models import User
from appointment.models import Appointment



@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def create_consultation(request,id):
    try:
        appointment = Appointment.objects.get(pk=id)
        
    except ObjectDoesNotExist:
        return Response({"error":"Doctor or patient not found"}, status=status.HTTP_404_NOT_FOUND)
    
    doctor = appointment.created_for
    patient = appointment.created_by
    


    admin = request.user
    if  admin.role != 'admin':
        return Response({'error': "Only admin can create consultation"}, status=status.HTTP_403_FORBIDDEN)

    consultation = Consultation.objects.create(created_for=doctor,created_by=admin,patient=patient,appointment=appointment)
    appointment.status = Appointment.PROCESSED
    appointment.save()

    serializer = ConsultationSerializer(consultation)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def get_sessions(request):
    doctor_sessions = DoctorSession.objects.filter(users__in=[request.user])

    # Serialize the queryset
    serializer = SessionSerializer(doctor_sessions, many=True)

    return Response(serializer.data)
     
    

@api_view(['POST'])
def get_or_create_doctor_session(request,id):
    try:
        patient = User.objects.get(pk=id)
        
    except ObjectDoesNotExist:
        return Response({"error":"Patient not found"}, status=status.HTTP_404_NOT_FOUND)
    
    doctor_sessions = DoctorSession.objects.filter(users__in=[request.user, patient]).distinct()
    
    if doctor_sessions.exists():
        doctor_session = doctor_sessions.first()
    else:
        doctor_session = DoctorSession.objects.create()
        doctor_session.users.add(patient,request.user)

    serializer = SessionDetailSerializer(doctor_session)

    return Response(serializer.data)


@api_view(['POST'])
def session_send_message(request,id):
    try:
        doctor_session = DoctorSession.objects.get(pk=id)
        print(doctor_session.id)

        
    except ObjectDoesNotExist:
        return Response({"error":"Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    for user in doctor_session.users.all():
            if user != request.user:
                sent_to = user


    session_message = DoctorSessionMessage.objects.create(
        doctor_session = doctor_session,
        body = request.data.get('message'),
        created_by = request.user,
        sent_to = sent_to
    )

    serializer = SessionMessageSerializer(session_message)
    return Response(serializer.data)
    

    

