from django.db import models
import uuid
from account.models import User
# Create your models here.

class Notification(models.Model):
    APPOINTMENT = 'appointment'
    CONSULTATION = 'consultation'
    MESSAGE = 'message'
    SESSION_START = 'session_start'
    SESSION_STOP = 'session_stop'


    NOTIFICATION_TYPE = (
        (APPOINTMENT, 'Appointment'),
        (CONSULTATION, 'consultation'),
        (MESSAGE, 'Message'),
        (SESSION_START, 'Session_start'),
        (SESSION_STOP, 'Session_end')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=NOTIFICATION_TYPE)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)