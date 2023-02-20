from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationForm
from .models import create_user_activity,UserProfile,AddressGlobal
from .tasks import send_registration_email
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .user_model_backend import PhoneNumberBackend
from django.contrib.auth.backends import ModelBackend

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
    
def dashboard(request):
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
    pass

@login_required
def add_adress(request):
    pass

@login_required
def delete_address(request,address_id):
    address = AddressGlobal.objects.get(id=address_id).delete()
    return HttpResponseRedirect()
    pass

@login_required
def set_default(request,address_id):
    address = AddressGlobal.objects.filter(user=request.user,is_default=True)
    address.is_default = False
    new_address = AddressGlobal.objects.get(id=address_id)
    new_address.is_default=True
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


