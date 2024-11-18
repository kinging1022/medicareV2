from django.contrib import admin

# Register your models here.
from .models import Consultation , DoctorSession, DoctorSessionMessage , Medications
admin.site.register(Consultation)
admin.site.register(DoctorSessionMessage)
admin.site.register(DoctorSession)
admin.site.register(Medications)
