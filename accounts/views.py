from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse,get_object_or_404
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.conf import settings
from .forms import RegistrationForm,AddressEditForm,AddressForm
from .models import create_user_activity,UserProfile,AddressGlobal,State
from .tasks import send_registration_email
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model,login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .user_model_backend import PhoneNumberBackend
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from oauth2_provider.views.generic import ProtectedResourceView

User = get_user_model()


@transaction.atomic()
def register_view(request):
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
    
    return render(request,'accounts/registration/register.html',{'form':form})

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
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/registration/activation_invalid.html')

@login_required()
def dashboard(request):
    if request.user.is_seller():
        return redirect("seller:dashboard")
        
    profile = UserProfile.objects.get(user=request.user)
    return render(request,'accounts/registration/profile.html',{'profile':profile})

def edit_profile(request):
    pass

class LoginView(LoginView):
    template_name = 'accounts/registration/login.html'
    success_url = '/dashboard'
    authentication_classes = [ModelBackend,PhoneNumberBackend]

@login_required()
def address(request):
    user = request.user
    address = AddressGlobal.objects.filter(user=user)
    return render(request,'accounts/address.html',{'address':address})


@login_required
def edit_address(request,address_id):
    if request.method == 'POST':
        address = AddressGlobal.objects.filter(id=address_id,user=request.user)
        form = AddressEditForm(instace=address,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("accounts:address"))
    else:
        form = AddressEditForm(instance=address)
    
    return render(request,'accounts/edit_address.html',{"form":form})

@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            y = State.objects.get(name=city)
            print(y)
            z = State.objects.filter(name=state).first()
            print(z)
            if y.price is not None and (z.price is None or y.price <= z.price):
                address.price = z.price
            elif z.price is not None:
                address.price = y.price
            address.save()
            return HttpResponseRedirect(reverse('accounts:address'))
    else:
        form = AddressForm()
    
    return render(request,'accounts/add_address.html',{'form':form})


@login_required
def delete_address(request,address_id):
    address = AddressGlobal.objects.get(id=address_id).delete()
    return HttpResponseRedirect(reverse('accounts:address'))
    

@login_required
def set_default(request,address_id):
    address = AddressGlobal.objects.filter(user=request.user, is_default=True).update(is_default=False)
    new_address = AddressGlobal.objects.filter(user=request.user,id=address_id).update(is_default=True)
    previous_url = request.META.get("HTTP_REFERER")
    if "checkout" in previous_url:
        return redirect("checkout:checkout")

    return HttpResponseRedirect(reverse('accounts:address'))


def get_city(request):
    if request.GET.get('action') == 'get':
        state_ajax = int(request.GET.get('city',None))
        state = State.objects.get(id=state_ajax)
        descendants = state.get_children()
        product_list = list(descendants.values('name','id'))
        response = JsonResponse({'city':product_list})
        return response
    return HttpResponse('There is an error on the click')

