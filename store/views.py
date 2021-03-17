from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress
    )
from .utils import cookieCart


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItem = cookieData['cartItem']

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
        cookieData = cookieCart(request)
        cartItem = cookieData['cartItem']
        order = cookieData['order']
        items = cookieData['items']


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
        cookieData = cookieCart(request)
        cartItem = cookieData['cartItem']
        order = cookieData['order']
        items = cookieData['items']


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

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                    customer = customer,
                    order = order,
                    address = data['shipping']['address'],
                    city = data['shipping']['city'],
                    state = data['shipping']['state'],
                    zipcode = data['shipping']['zipcode'],
                )

    else:
        print('user is not logged in... ')

    return JsonResponse('pyment complete', safe=False)
