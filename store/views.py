from django.http.response import JsonResponse
import datetime
from .models import (Customer
                ,Order
                ,Product
                ,OrderItem
                ,ShippingAddress)
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .utils import *
# Create your views here.
def store(request):
    cart = cartData(request)
    orderitem = cart['orderitem']

    context = {'products':Product.objects.all(),'orderitem':orderitem}
    return render(request,'store/store.html',context)

#Updating Order
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    else:
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

#Order Information
def cart(request):
    cart = cartData(request)
    items = cart['items']
    order = cart['order']
    orderitem = cart['orderitem']

    context = {'items':items,'order':order,'orderitem':orderitem}
    return render(request,'store/cart.html',context)
#Payment checkpoint
def checkout(request):
    cart = cartData(request)
    items = cart['items']
    order = cart['order']
    orderitem = cart['orderitem']
 
    context = {'items':items,'order':order,'orderitem':orderitem}
    return render(request,'store/checkout.html',context)

#Saving info for future purposes
def processOrder(request):
    precessAndSave(request)

    return JsonResponse('Order is placed',safe=False)
