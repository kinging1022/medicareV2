from django.db import models
import uuid
from django.utils.timesince import timesince
from account.models import User
# Create your models here.
class Appointment(models.Model):

    SENT = 'sent'
    PROCESSED = 'processed'
    DONE = 'done'

    STATUS_CHOICES = (
        (SENT,'Sent'),
        (PROCESSED,'Processed'),
        (DONE, 'Done')
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='appointment_by', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='appointment_for', on_delete=models.CASCADE ,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,  choices=STATUS_CHOICES, default=SENT)


    class Meta:
        ordering = ('-created_at',)


    def created_at_formatted(self):
        return timesince(self.created_at)
    
    
