from django.db import models
import uuid
from account.models import User

# Create your models here.

class UserCredit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credits')
    total_credits = models.PositiveIntegerField(default=0)





class CreditTransaction(models.Model):
    CREDIT = 'credit'
    DEBIT = 'debit'
    type = (
        (CREDIT,'Credit'),
        (DEBIT, 'Debit'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField()
    message = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50,  choices=type, default=CREDIT)

    timestamp = models.DateTimeField(auto_now_add=True)
    payment_intent = models.CharField(max_length=200, null=True, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)


class CreditPrice(models.Model):
    price_per_credit = models.DecimalField(max_digits=6, decimal_places=2)
    effective_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Price: ${self.price_per_credit} (Effective: {self.effective_date})"
    

    
