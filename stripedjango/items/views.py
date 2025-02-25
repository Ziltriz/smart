from django.shortcuts import render, get_object_or_404
from django.conf import settings
import stripe
from django.http import JsonResponse, HttpResponseServerError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from .serializers import OrderSerializer
from .models import Order, Item
from .services import create_payment_intent
from stripe import StripeClient
from rest_framework.permissions import AllowAny




class CreatePaymentIntentView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, order_id):
        try:
            client_secret = create_payment_intent(order_id)
            return Response({'client_secret': client_secret}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    

    context = {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret':''
    }
    return render(request, 'items/item_detail.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,

    }
    return render(request, 'items/order_detail.html', context)


def success(request):
    return render(request, 'items/success.html')

def error_page(request):
    return render(request, 'items/error.html')

def create_checkout_session(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    try:
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100), 
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )
    except stripe.error.AuthenticationError as e:
        # Ошибка аутентификации (неверный API-ключ)
        print(f"Authentication Error: {e}")
        return HttpResponseServerError("Invalid API key. Please check your Stripe credentials.")
    
    except stripe.error.InvalidRequestError as e:
        # Ошибка запроса (например, неверная валюта или цена)
        print(f"Invalid Request Error: {e}")
        return HttpResponseServerError("Invalid request parameters. Please check the item details.")
    
    except Exception as e:
        # Обработка других ошибок
        print(f"Unexpected Error: {e}")
        return HttpResponseServerError("An unexpected error occurred. Please try again later.")

    return JsonResponse({'id': session.id})