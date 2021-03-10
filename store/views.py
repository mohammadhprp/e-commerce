from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress
    )
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False
        }
        cartItem = order['get_cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItem': cartItem
    }
    return render(request, 'store/Store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False
        }
        cartItem = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItem': cartItem
    }
    return render(request, 'store/Cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items

    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False
        }
        cartItem = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cartItem': cartItem
    }
    return render(request, 'store/Checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('productId:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity  + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity  - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

        #30:00
    return JsonResponse('Item was added', safe=False)
