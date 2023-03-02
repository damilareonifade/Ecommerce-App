import asyncio
import aiohttp
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

async def payment(request):
    # Set up the payment parameters
    payload = {
        'tx_ref': 'unique_transaction_reference',
        'amount': '100',
        'currency': 'NGN',
        'redirect_url': request.build_absolute_uri(reverse('payment_callback')),
        'payment_options': 'card',
        'meta': {
            'user_id': request.user.id,
            'email': request.user.email,
        },
        'customer': {
            'email': request.user.email,
            'phonenumber': '08012345678',
            'name': request.user.get_full_name(),
        },
        'customizations': {
            'title': 'My Online Store',
            'description': 'Payment for items in cart',
            'logo': 'https://example.com/logo.png',
        }
    }

    # Generate the payment link
    headers = {'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post('https://api.flutterwave.com/v3/payments', json=payload) as response:
            if response.status == 200:
                payment_url = (await response.json())['data']['link']
                return redirect(payment_url)
            else:
                # Handle the error case
                pass

from django.shortcuts import render

def payment_callback(request):
    transaction_id = request.GET.get('transaction_id')
    transaction_reference = request.GET.get('tx_ref')
    status = request.GET.get('status')
    amount = request.GET.get('amount')

    # Handle the payment response
    if status == 'successful':
        # Payment was successful
        return render(request, 'payment_success.html', {'amount': amount})
    else:
        # Payment was not successful
        return render(request, 'payment_error.html')
