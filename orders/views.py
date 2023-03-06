from django.shortcuts import render,HttpResponseRedirect,HttpResponse
import aiohttp
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
import asyncio
from cart.basket import Basket
import string
import random
from asgiref.sync import sync_to_async,async_to_sync

def check_payment(request):
    if 'purchase' in request.session and 'delivery_id' in request.session['purchase']:
        return HttpResponseRedirect(reverse('orders:make_payment'))
        
    else:
        messages.info(request,'Select a Delivery Option')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

async def make_payment(request):  
    user = await sync_to_async(lambda: request.user)()
    basket = await sync_to_async(Basket)(request)
    digits = ''.join(random.choices(string.digits, k=4))
    strings = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=4))
    tx_ref = strings + digits

    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": settings.FLUTTERWAVE_SECRET_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "tx_ref": tx_ref,
        "amount": 1000,
        "currency": "NGN",
        "payment_options": "card",
        "customer": {
            "email": await sync_to_async(lambda: request.user.email)(),
        },
        "redirect_url": "http://example.com/redirect",
        "meta": {
            "user_id": user.id,
            "invoice_id": "67890"
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,headers=headers, json=data) as response:
            response_data = await response.json()
            if response_data['status'] == 'success':
                z = response_data['data']['link']
                return HttpResponseRedirect(z)
            else:
                return HttpResponse('Guy something is wrong')


def payment_callback(request):
    if request.method == 'POST':
        # Retrieve the transaction reference from the request data
        tx_ref = request.POST.get('tx_ref')

        # Perform any necessary database updates or business logic
        # based on the payment status and transaction reference

        # Return a success response to the Flutterwave payment gateway
        return HttpResponseRedirect('Payment successful')