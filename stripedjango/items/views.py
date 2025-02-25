from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Item



def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    context = {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'items/item_detail.html', context)

