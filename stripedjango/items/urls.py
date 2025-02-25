from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('buy/<int:item_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),  
    path('api/create-payment-intent/<int:order_id>/', views.CreatePaymentIntentView.as_view(), name='create_payment_intent'),  
    path('api/orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail_api'), 
    path('success/', views.success, name='success'),
    path('cancel/', views.error_page, name='canceled_pay')
]