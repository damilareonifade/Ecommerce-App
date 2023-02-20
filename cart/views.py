from django.shortcuts import render
from django.urls import reverse
from commerce.models import Product
from .basket import Basket
import json
from accounts.models import AddressGlobal
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

@login_required()
def checkout(request):
    user = request.user
    user_address = AddressGlobal.objects.filter(user=request.user,is_default=True)
    if not user_address:
        return reverse('accounts:address')
    
    return render(request,'basket/checkout.html',{'address':user_address})