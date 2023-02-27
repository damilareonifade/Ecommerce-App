from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from commerce.models import Product
from .basket import Basket
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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


def basket_all(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket':basket})


def basket_update(request):
    pass

def basket_delete(request):
    basket = Basket(request)
    user = request.user
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price(user)
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
