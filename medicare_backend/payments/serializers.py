from rest_framework import serializers
from account.serializers import UserSerializer
from .models import CreditTransaction, UserCredit

class CreditTransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CreditTransaction
        fields = ('id','user','amount','message','type','timestamp','paid')





class UserCreditSerializer(serializers.ModelSerializer):
        
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserCredit
        fields = ('user','total_credits')


    