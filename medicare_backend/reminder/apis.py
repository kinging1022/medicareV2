from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Reminder 
from consultations.models import Medications
from consultations.serializers import MedicationsSerializer



@api_view(['POST'])
def set_reminder(request,id):
    try:
        medication = Medications.objects.get(pk=id)
    except Medications.DoesNotExist:
        return Response({'error': 'medication not found'},status=status.HTTP_400_BAD_REQUEST)
    


    reminder = Reminder.objects.create(
        medication = medication,
        user = request.user,
        email = request.data.get('email'),
        time = request.data.get('time'),
        phone = request.data.get('phoneNumber'),
        message = f"Reminder created for {medication.name}"


    )

    medication.has_reminder = True
    medication.save()

    serializer = MedicationsSerializer(medication)

    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def delete_reminder(request,id):
    try:
        medication = Medications.objects.get(pk=id)
    except Medications.DoesNotExist:
        return Response({'error': 'medication not found'},status=status.HTTP_400_BAD_REQUEST)
    


    reminder = Reminder.objects.get(medication=medication)
    reminder.delete()

    medication.has_reminder = False
    medication.save()

    serializer = MedicationsSerializer(medication)

    return Response(serializer.data, status=status.HTTP_200_OK)

