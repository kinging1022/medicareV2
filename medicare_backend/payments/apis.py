import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import CreditPrice
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import CreditTransaction, UserCredit
from .serializers import CreditTransactionSerializer, UserCreditSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET'])
def get_credit_price(request):
    try:
        latest_price = CreditPrice.objects.latest('effective_date')
        return Response({'credit_price': float(latest_price.price_per_credit)})
    except CreditPrice.DoesNotExist:
        return Response({'error': 'No price set yet.'}, status=404)
    




@api_view(['GET'])
def get_transaction(request):
    transactions = CreditTransaction.objects.filter(user=request.user, paid=True)

    serializer = CreditTransactionSerializer(transactions, many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)




@api_view(['GET'])
def get_credits(request):
    try:
        user_credit = UserCredit.objects.get(user=request.user)
    except UserCredit.DoesNotExist:
        return Response({'message':'No user credit'},status=status.HTTP_204_NO_CONTENT)

    serializer = UserCreditSerializer(user_credit)

    return Response(serializer.data,status=status.HTTP_200_OK)







@api_view(['POST'])
@csrf_exempt
def checkout(request):
    quantity = request.data.get('quantity',1)
    credit_price = request.data.get('price')

    amount = int(quantity) * int(credit_price)

    transaction = CreditTransaction.objects.create(user = request.user, amount=amount, type=CreditTransaction.CREDIT)


    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'{quantity} Session Credit{"s" if quantity > 1 else ""}',
                        },
                        'unit_amount': credit_price * 100,  
                    },
                    'quantity': quantity,
                },
            ],
            mode='payment',
            payment_intent_data={
                'metadata':{
                    'transaction_id' : transaction.id,
                    'quantity': quantity,
                }
            },
            success_url=f'http://127.0.0.1:8000/payment-success/?transaction_id={transaction.id}',

            cancel_url='http://127.0.0.1:8000/payment-cancel/',
        )
        return Response({'sessionId':session.id})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


