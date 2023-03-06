from django.shortcuts import render,get_object_or_404,redirect
from .models import DeliveryOptions,PaymentSelections
from accounts.models import AddressGlobal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.basket import Basket
from django.urls import reverse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import DeliveryOptions
from django.http import Http404


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    my_address = AddressGlobal.objects.filter(user=request.user)
    user_address = AddressGlobal.objects.filter(user=request.user,is_default=True)
    if not user_address:
        messages.warning(request,'You have to create an address before going to checkout')
        return HttpResponseRedirect(reverse('accounts:address'))  

    for address in user_address:
        addresses = address.state.price        
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions,'addresses':my_address,'price':addresses})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        address = AddressGlobal.objects.get(user=request.user,is_default=True)
        deliveryprice = int(delivery_type.delivery_price) + int(address.state.price)
        updated_total_price = basket.basket_update_delivery(deliveryprice)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,"address_id":address.id
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session["purchase"]['address_id'] = address.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": deliveryprice})
        return response

@login_required()
def checkout(request):
    user = request.user
    basket = Basket(request)
    user_address = AddressGlobal.objects.filter(user=user,is_default=True)
    if not user_address:
        return HttpResponseRedirect(reverse('accounts:address'))  

    for address in user_address:
        addresses = address.state.price        

    return render(request,'basket/checkout.html',{'address':user_address,'address_price':addresses})

@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = AddressGlobal.objects.filter(customer=request.user,is_default=True)

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META.get["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})




