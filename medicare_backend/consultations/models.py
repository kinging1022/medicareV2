from django.db import models
import uuid
from django.utils.timesince import timesince
from account.models import User
from appointment.models import Appointment
from account.models import User
from django.utils.dateformat import format
from django.utils.timezone import localtime


# Create your models here.
class Consultation(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
         (SENT,'Sent'),
         (ACCEPTED,'Accepted'),
         (REJECTED, 'Rejected'),
     )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(Appointment,related_name='appointments',on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=SENT)
    created_by = models.ForeignKey(User, related_name='created_consultation',on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='recieved_consultation',on_delete=models.CASCADE )
    patient = models.ForeignKey(User, related_name='requested_consultation',on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('created_at',)


    def created_at_formatted(self):
        return timesince(self.created_at)
    

class DoctorSession(models.Model):
    STARTED = 'started'
    ENDED = 'ended'
    STATUS_CHOICES = (
        (STARTED,'Started'),
        (ENDED, 'Ended'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation = models.ForeignKey(Consultation,related_name='consultations', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='doctor_session')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def modified_at_formatted(self):
        return timesince(self.created_at)
    
class DoctorSessionMessage(models.Model):
    TEXT = 'text'
    NOTIFICATION = 'notification'

    MESSAGE_CHOICE = (
        (TEXT, 'Text'),
        (NOTIFICATION, 'Notification'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_session = models.ForeignKey(DoctorSession, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    type = models.CharField(max_length=50, choices=MESSAGE_CHOICE, default=TEXT)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sentmessages', on_delete=models.CASCADE)

    def created_at_formatted(instance):
        return format(localtime(instance.created_at), 'Y-m-d\TH:i:s\Z')



    
class Medications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_session = models.ForeignKey(DoctorSession,related_name='medications', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    weight = models.CharField(max_length=10)
    dosage = models.TextField()
    created_by = models.ForeignKey(User, related_name='medication_by', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='medications_for', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def created_at_formatted(self):
        return timesince(self.created_at)
