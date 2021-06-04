import json
from .models import *
import datetime

def getcookie(request):
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order={'get_total_item':0,'get_total_price':0,'isallDigital':True}
        
        for id in cart:
            try:
                item = {
                    'product':{
                        'name':'',
                        "price":0,
                        'image':0,
                        'id':0
                    },
                    'get_total':0,
                    'quantity':0
                }
                product = Product.objects.get(id=int(id))
                order['get_total_item'] += cart[id]['quantity']
                order['get_total_price'] += product.price*cart[id]['quantity'] 
                item['quantity'] = cart[id]['quantity']
                item['get_total'] = product.price*item['quantity']
                item['product']['name'] = product.name
                item['product']['price'] = product. price
                item['product']['image'] = product.image
                item['product']['id'] = product.id

                items.append(item)

                if product.digital != 'True' :
                    order['isallDigital'] = False
            except:
                pass

        orderitem = order['get_total_item']
        return {'items':items,'order':order,'orderitem':orderitem}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        orderitem =  order.get_total_item
                
    else:
        cart = getcookie(request)
        items = cart['items']
        order = cart['order']
        orderitem = cart['orderitem']

    
    return {'items':items,'order':order,'orderitem':orderitem}

def precessAndSave(request):

    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = Customer.objects.get_or_create(request.user)
    else:
        name = data['userinfo']['name']
        email = data['userinfo']['name']
        customer, created = Customer.objects.get_or_create(name=name,email=email)
        customer.save()


    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    order.transaction_id = datetime.datetime.now().timestamp()

    if float(data['userinfo']['total']) == order.get_total_price:
       order.complete   = True
    order.save()

    if not order.isallDigital:
        
        ShippingAddress.objects.create(
                                       customer=customer,order=order,
                                       state=data['shippinginfo']['state'],
                                       city=data['shippinginfo']['city'],
                                       zipcode=data['shippinginfo']['zipcode'],
                                       address=data['shippinginfo']['address']
                                    )
    