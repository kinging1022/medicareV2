from django.db import models
import uuid
from django.utils.timesince import timesince
from account.models import User
from appointment.models import Appointment
from account.models import User
from django.utils.dateformat import format
from django.utils.timezone import localtime


# Create your models here.
from django.core.exceptions import ValidationError
import os

def validate_file(file):
   
    # File size limit (5 MB)
    max_file_size = 5 * 1024 * 1024

    # Allowed file extensions
    allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    allowed_video_extensions = ['.mp4', '.avi', '.mov', '.mkv']

    # Get the file extension
    file_extension = os.path.splitext(file.name)[1].lower()

    # Check file size
    if file.size > max_file_size:
        raise ValidationError(f"File size exceeds the limit of {max_file_size / (1024 * 1024)} MB.")

    # Check file extension
    if file_extension in allowed_image_extensions:
        # Valid image
        return
    elif file_extension in allowed_video_extensions:
        # Valid video
        return
    else:
        raise ValidationError("Unsupported file type. Allowed formats: images (.jpg, .jpeg, .png, .gif) and videos (.mp4, .avi, .mov, .mkv).")


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
    IMAGE = 'image'
    VIDEO = 'video'

    MESSAGE_CHOICE = (
        (TEXT, 'Text'),
        (NOTIFICATION, 'Notification'),
        (IMAGE,'Image'),
        (VIDEO,'Video')

    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_session = models.ForeignKey(DoctorSession, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    type = models.CharField(max_length=50, choices=MESSAGE_CHOICE, default=TEXT)
    image = models.ImageField(upload_to='media/chat_images/', blank=True, null=True, validators=[validate_file])
    video = models.FileField(upload_to='media/chat_videos/', blank=True, null=True, validators=[validate_file])
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sentmessages', on_delete=models.CASCADE)

    def created_at_formatted(instance):
        return format(localtime(instance.created_at), 'Y-m-d\TH:i:s\Z')
    

    def get_image(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        

    def get_video(self):
        if self.video:
           return "http://127.0.0.1:8000" + self.video.url



    
class Medications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_session = models.ForeignKey(DoctorSession,related_name='medications', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    weight = models.CharField(max_length=10)
    dosage = models.TextField()
    created_by = models.ForeignKey(User, related_name='medication_by', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='medications_for', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    has_reminder = models.BooleanField(default=False)


    def created_at_formatted(self):
        return timesince(self.created_at)
