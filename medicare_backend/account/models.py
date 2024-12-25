from django.db import models
from datetime import date

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        
        if self.model.objects.filter(email=email).exists():
            raise ValueError("A user with this email exist ")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):

    PATIENT = 'patient'
    DOCTOR = 'doctor'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (ADMIN, 'Administrator')
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False )
    email = models.EmailField(unique=True, max_length=225)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, null=True, blank=True)
    allergies = models.CharField(max_length=500, blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    blood_type = models.CharField(max_length=10,blank=True,null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PATIENT)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.CharField(max_length=200, blank=True, null=True)
    timezone = models.CharField(max_length=200, blank=True, null=True)


    def display_age(self):
        if isinstance(self.dob, date):
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month,self.dob.day))
            return age
        return None
    
    def unread_notification_count(self):
        total_notifications = self.received_notifications.count()
        read_notification = self.received_notifications.filter(is_read=True).count()

        return total_notifications - read_notification






    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'role','gender','dob']

    def __str__(self):
        return self.email

