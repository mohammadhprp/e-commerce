from django.shortcuts import render
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress
    )
def store(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/Store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/Cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/Checkout.html', context)
