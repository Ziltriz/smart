from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('buy/<int:item_id>/', views.create_checkout_session, name='create_checkout_session'),
]