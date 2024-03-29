from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from commerce.models import Product
from .basket import Basket
import json
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction

transaction.atomic()
def basket_add(request):
    # add product,seller,attribute,author to the basket  session for later processing
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("productid",None))
        product_qty = int(request.POST.get('qty',None))
        product = Product.objects.get(id=product_id)
        author = product.seller
        selected_values = json.loads(request.POST.get('selected_values'))
        y = []
        #Iterated through the attribute_values coming from the frontend and add to the basket session
        if selected_values:
            for attribute_name, attribute_value in selected_values.items():
                y.append(attribute_name)  
                basket.add(product=product,product_qty=product_qty,seller=author,attribute_name=y)

        # if product.product_stock.in_stock < product_qty:
        #     messages.info(request,"The product is sold out you can check other vendors")
        #     response = JsonResponse({"qty":'Product is sold out'})
        #     return response
        basketqty = basket.__len__()
        response = JsonResponse({'qty':basketqty})
        return response


def basket_all(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket':basket})


def basket_update(request):
    pass

@transaction.atomic()
def basket_delete(request):
    basket = Basket(request)
    user = request.user
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_subtotal_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
