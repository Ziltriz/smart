import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(order_id):
    from .models import Order

    order = Order.objects.get(id=order_id)
    amount = int(order.total_price * 100)  

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=order.currency,
        automatic_payment_methods={'enabled': True},
    )
    return intent.client_secret