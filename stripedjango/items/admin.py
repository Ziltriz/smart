from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    filter_horizontal = ('items',)
    list_display = ( 'discount', 'tax', 'currency', 'total_price')
    list_filter = ('currency',)
    search_fields = ('items__name',)  


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')