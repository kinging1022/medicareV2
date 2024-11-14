from rest_framework import serializers
from .models import Consultation , DoctorSession, DoctorSessionMessage
from account.serializers import UserSerializer
from appointment.serializers import AppointmentSerializer



class ConsultationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = ('id','appointment','created_by','created_for','patient','created_at','status','created_at_formatted')



class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSession
        fields = ('id', 'users', 'status', 'modified_at_formatted',)
    
    

class SessionMessageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = DoctorSessionMessage
        fields = ('id','created_by', 'created_at_formatted','body',)


class SessionDetailSerializer(serializers.ModelSerializer):
    messages = SessionMessageSerializer(read_only=True, many=True)

    class Meta:
        model = DoctorSession
        fields = ('id', 'users', 'status', 'modified_at_formatted', 'messages',)
        

   
    
    