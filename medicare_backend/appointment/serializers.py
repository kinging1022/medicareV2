from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id','body','status','created_at','created_by','created_at_formatted','created_for')

