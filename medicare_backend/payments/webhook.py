import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import UserCredit, CreditTransaction



stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(f"Error parsing webhook data: {e}")
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object 
        print(f"Payment Intent ID: {payment_intent.id}")
        try:
            
            quantity = int(payment_intent['metadata'].get('quantity', 0))
            transaction_id = payment_intent['metadata'].get('transaction_id')

            transaction = CreditTransaction.objects.get(pk=transaction_id)
            transaction.message = f"Bought {quantity} session{'s' if quantity > 1 else ''} credit"
            transaction.payment_intent = payment_intent.id  
            transaction.paid = True
            transaction.save()

            user = transaction.user  
            usercredit, created = UserCredit.objects.get_or_create(user=user)
            usercredit.total_credits += quantity
            usercredit.save()

        except ObjectDoesNotExist:
            print(f"Transaction not found for payment intent {payment_intent.id}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)
