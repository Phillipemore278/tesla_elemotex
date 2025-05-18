from django.shortcuts import get_object_or_404, render

from .models import Order

def order_successful(request, order_key):
    order = get_object_or_404(Order, order_key=order_key)
    return render(request, 'order/order_successful.html', {'order': order})
