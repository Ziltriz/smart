from stripe import StripeClient
from django.conf import settings



def create_payment_intent(order_id):
    from .models import Order
    client = StripeClient(settings.STRIPE_PUBLIC_KEY)
    order = Order.objects.get(id=order_id)
    amount = int(order.total_price * 100)  

    intent = client.PaymentIntent.create(
        amount=amount,
        currency=order.currency,
        automatic_payment_methods={'enabled': True},
    )
    return intent.client_secret