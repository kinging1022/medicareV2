from .models import Notification
from django.db import transaction

def create_notification(created_by, created_for, notification_type):
    messages = {
        'appointment': f'A new appointment was created by {created_by.first_name} {created_by.last_name}',
        'consultation_doctor': f'A consultation request was created for {created_by.first_name} {created_by.last_name}',
        'consultation_patient': f'Your appointment request has been processed and your doctor will contact you soon',
        'session_start_patient': f'Dr {created_by.first_name} created a session',
        'session_start_doctor': f'You started a session with {created_by.first_name} {created_by.last_name}',
        'session_stop_patient': f'Your session with Dr {created_by.first_name} has ended'
    }
    
    role_key = f"{notification_type}_{created_for.role}" if notification_type in ['consultation', 'session_start', 'session_stop'] else notification_type
    
    body = messages.get(role_key, "A new notification was created")
    
    with transaction.atomic():
        notification = Notification.objects.create(
            created_by=created_by,
            created_for=created_for,
            type_of_notification=notification_type,
            body=body
        )
        
       

    return notification
