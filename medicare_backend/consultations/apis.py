from rest_framework.decorators import api_view, authentication_classes , permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ConsultationSerializer , SessionDetailSerializer,MedicationsSerializer, SessionMessageSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import Consultation , DoctorSession, Medications, DoctorSessionMessage
from account.models import User
from appointment.models import Appointment
from notification.utils import create_notification
from notification.models import Notification
from payments.models import UserCredit, CreditTransaction, CreditPrice



from django.db import transaction, IntegrityError


@api_view(['POST'])
def create_consultation(request, id):
    try:
        appointment = Appointment.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({"error": "Appointment with the given ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

    doctor = appointment.created_for
    patient = appointment.created_by
    admin = request.user

    if admin.role != 'admin':
        return Response({'error': "Only admin can create a consultation"}, status=status.HTTP_403_FORBIDDEN)

    consultation = Consultation.objects.create(
        created_for=doctor,
        created_by=admin,
        patient=patient,
        appointment=appointment
    )

    create_notification(patient, doctor, Notification.CONSULTATION)
    

    appointment = Appointment.objects.select_for_update().get(id=appointment.id)
    appointment.status = Appointment.PROCESSED
    appointment.save()
    create_notification(admin, patient, Notification.CONSULTATION)

    serializer = ConsultationSerializer(consultation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

     
    

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
    
    with transaction.atomic():

        doctor_sessions = DoctorSession.objects.filter(users__in=[request.user, patient]).distinct()

        if doctor_sessions.exists():
            doctor_session = doctor_sessions.first()
            doctor_session.status = DoctorSession.STARTED
            doctor_session.save()
        else:
            doctor_session = DoctorSession.objects.create(consultation=consultation)
            doctor_session.users.add(patient, request.user)
            
            
        doctor = consultation.created_for 
        notification = create_notification(doctor,patient,Notification.SESSION_START)


        consultation.status = Consultation.ACCEPTED
        consultation.save()
           

            

        serializer = SessionDetailSerializer(doctor_session)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def get_active_session(request):
    try:
        session = DoctorSession.objects.get(users=request.user,status=DoctorSession.STARTED)

    except DoctorSession.DoesNotExist:
        return Response({'message':'No active session'}, status=status.HTTP_204_NO_CONTENT)


    serializer = SessionDetailSerializer(session)

    return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['GET'])
def view_session(request,id):
    try:
        doctor_session = DoctorSession.objects.get(pk=id)

    except DoctorSession.DoesNotExist:
        return Response({'error':'session not found'},status=status.HTTP_400_BAD_REQUEST)
    
    serializer = SessionDetailSerializer(doctor_session)

    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
def session_history(request):
    sessions = DoctorSession.objects.filter(users=request.user, status=DoctorSession.ENDED)

    serializer = SessionDetailSerializer(sessions, many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)

   
@api_view(["POST"])
def send_message(request, id):
    try:
        session = DoctorSession.objects.get(pk=id)
    except DoctorSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    image = None
    video = None
    message_type = 'text' 

    file = request.FILES.get('file')
    if file and file.size > 0:
        mime_type = file.content_type
        if mime_type.startswith('image/'):
            message_type = 'image'
            image = file
        elif mime_type.startswith('video/'):
            message_type = 'video'
            video = file
        else:
            return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        message_type = request.data.get('type')
        if not message_type or message_type not in ['text', 'notification']:
            return Response({"error": "Invalid or missing message type"}, status=status.HTTP_400_BAD_REQUEST)

    message = DoctorSessionMessage.objects.create(
        doctor_session=session,
        body=request.data.get('body', ''),
        created_by=request.user,
        type=message_type,
        image=image,
        video=video
    )
    
    serializer = SessionMessageSerializer(message)
    return Response(serializer.data)

   
    


@api_view(['POST'])
def end_session(request, id):
    try:
        doctor_session = DoctorSession.objects.get(pk=id)
    except DoctorSession.DoesNotExist:
        return Response({'error': "Doctor session not found"}, status=status.HTTP_404_NOT_FOUND)

    patient = doctor_session.users.exclude(pk=request.user.id).filter(role='patient').first()
    
    if not patient:
        return Response({'error': 'Unable to identify patient'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_credit = UserCredit.objects.get(user=patient)
    except UserCredit.DoesNotExist:
        return Response({'error': 'User credit not found'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        doctor_session.status = DoctorSession.ENDED
        doctor_session.save()

        try:
            appointment = Appointment.objects.get(created_by=patient, status=Appointment.PROCESSED)
        except Appointment.DoesNotExist:
            return Response({'error': 'No processed appointment found for the patient'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = Appointment.DONE
        appointment.save()

        if user_credit.total_credits > 0:
            user_credit.total_credits -= 1
          
        user_credit.save()

        latest_price = CreditPrice.objects.latest('effective_date')
        amount = latest_price.price_per_credit

        message = f'Debited 1 session credit for session with Dr {request.user.first_name}'
        credit_transaction = CreditTransaction.objects.create(
            user=patient,
            amount=amount,
            message=message,
            type=CreditTransaction.DEBIT,
            paid=True
        )

        serializer = SessionDetailSerializer(doctor_session)

        try:
            create_notification(request.user, patient, Notification.SESSION_STOP)
        except Exception as e:
            return Response({'error': f"Failed to create notification: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(
        {
            'data': serializer.data,
            'message': f'Dr. {request.user.first_name} ended the session'
        },
        status=status.HTTP_200_OK
    )



@api_view(['POST'])
def add_medications(request, id):
    try:
        doctor_session = DoctorSession.objects.get(pk=id)
    except DoctorSession.DoesNotExist:
        return Response({'error': "Doctor session not found"}, status=status.HTTP_404_NOT_FOUND)

    medications_data = request.data
    if not medications_data or not isinstance(medications_data, list):
        return Response({"error": "Invalid or empty data format. Expected a non-empty array of objects."}, status=status.HTTP_400_BAD_REQUEST)

    users = doctor_session.users
    try:
        patient = users.exclude(pk=request.user.id).filter(role='patient').first()
    except Exception as e:
        return Response({'error': f"Error identifying patient: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not patient:
        return Response({'error': 'Unable to identify patient'}, status=status.HTTP_400_BAD_REQUEST)

    medications = [
        Medications(
            doctor_session=doctor_session,
            name=data.get('medication'),
            weight=data.get('weight'),
            dosage=data.get('dosage'),
            created_by=request.user,
            created_for=patient
        )
        for data in medications_data if all([data.get('medication'), data.get('weight'), data.get('dosage')])
    ]

    if len(medications) != len(medications_data):
        return Response({"error": "Missing fields in some prescriptions"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        Medications.objects.bulk_create(medications)
    except Exception as e:
        return Response({'error': f'Failed to add medications: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': f'{len(medications)} medications were added to this session'}, status=status.HTTP_201_CREATED)





