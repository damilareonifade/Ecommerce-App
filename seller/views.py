from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .permissions import seller
from .forms import RegistrationForm
from accounts.models import create_user_activity
from commerce.models import Product
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model,login
from accounts.tasks import send_registration_email
from django.db import transaction
from django.db.models import Sum,F

User = get_user_model()

@transaction.atomic()
def seller_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.is_active = False
            user.save()
            action = "User Created"
            create_user_activity(user,action)
            # send_registration_email.apply_async(args=[user])
            return redirect(reverse('accounts:register_successfully'))
    else:
        form = RegistrationForm(request.POST)
    return render(request,"adminstrative/register.html",{'form':form})

@transaction.atomic()
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('seller:seller_dashboard')
    else:
        return render(request, 'accounts/registration/activation_invalid.html')

@login_required
def seller_dashboard(request):
    user = request.user
    amt_of_product_avail = Product.objects.filter(seller_id=1).aggregate(total_price=Sum(F('showed_price') * F('product_stock__in_stock')))['total_price']
    amt_of_product_sold = Product.objects.filter(seller_id=1).aggregate(total_price=Sum(F('showed_price') * F('product_stock__sold_stock')))['total_price']

