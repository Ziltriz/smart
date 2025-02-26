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
    list_display = ('name', 'get_percentage', 'amount_off', 'currency', 'duration', 'duration_in_months')
   
    def get_percentage(self, obj):
        return f"{obj.percentage}%" if obj.percentage is not None else "—"

    get_percentage.short_description = 'Percentage Off'

    list_filter = ('duration',)
    search_fields = ('name',)

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')