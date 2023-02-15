from django.shortcuts import render
from commerce.models import Product
from .basket import Basket
import json
from django.http import JsonResponse


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("productid",None))
        product_qty = int(request.POST.get('qty',None))
        product = Product.objects.get(id=product_id)
        basket.add(product=product,product_qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty':basketqty})
        return response

