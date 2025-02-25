from rest_framework import serializers
from .models import Item, Order, Discount, Tax

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price', 'currency')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'name', 'percentage')

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ('id', 'name', 'percentage')

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    discount = DiscountSerializer(read_only=True)
    tax = TaxSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'items', 'discount', 'tax', 'currency', 'total_price')