from django.contrib import admin
from .models import CreditTransaction, UserCredit, CreditPrice

# Register your models here.
admin.site.register(CreditPrice)
admin.site.register(CreditTransaction)
