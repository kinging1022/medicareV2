from rest_framework.decorators import api_view, authentication_classes , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ConsultationSerializer , SessionDetailSerializer, SessionSerializer, MedicationsSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import Consultation , DoctorSession, Medications
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
def get_or_create_doctor_session(request, consultation_id, patient_id):
    try:
        patient = User.objects.get(pk=patient_id)
    except User.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        consultation = Consultation.objects.get(pk=consultation_id)
    except Consultation.DoesNotExist:
        return Response({"error": "Consultation not found"}, status=status.HTTP_404_NOT_FOUND)

    doctor_sessions = DoctorSession.objects.filter(users__in=[request.user, patient]).distinct()

    if doctor_sessions.exists():
        doctor_session = doctor_sessions.first()
    else:
        doctor_session = DoctorSession.objects.create(consultation=consultation)
        doctor_session.users.add(patient, request.user)

        consultation.status = Consultation.ACCEPTED
        consultation.save()

    serializer = SessionDetailSerializer(doctor_session)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_medications(request, id):
    try:
        doctor_session = DoctorSession.objects.get(pk=id)
    except DoctorSession.DoesNotExist:
        return Response({'error':"Doctor session not found "},status=status.HTTP_400_BAD_REQUEST)
    
    medications_data = request.data

    if not isinstance(medications_data,list):
        return Response({"error":"Invalid data format. Expected. Expected an array of objects"},status=status.HTTP_400_BAD_REQUEST)

    for medications_data in medications_data:
        name = medications_data.get('medication')
        weight = medications_data.get('weight')
        dosage = medications_data.get('dosage')

        if not all([name,weight,dosage]):
            return Response({"error":"Missing fields in prescription data"}, status=status.HTTP_400_BAD_REQUEST)

        medication = Medications.objects.create(doctor_session=doctor_session,  name=name, weight=weight, dosage= dosage)

    serializer = MedicationsSerializer(medication)
    return Response({'message':'medication was added to this session'},status=status.HTTP_201_CREATED)






    

    

