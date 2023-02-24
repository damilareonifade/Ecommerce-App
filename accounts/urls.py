from django.urls import path 
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import (LogoutView,PasswordChangeDoneView,PasswordResetView,
PasswordChangeView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView)
from .user_model_backend import PhoneNumberBackend
from django.contrib.auth.backends import ModelBackend
from .views import LoginView


app_name = 'accounts'

authen = [ModelBackend,PhoneNumberBackend]

urlpatterns = [
    path('register/',views.register_view,name='register'),  
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='/accounts/login'),name='logout'),
    
    path('register/successfully/',TemplateView.as_view(template_name='accounts/registration/register_succesfully.html'),name='register_successfully'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate,name='activate'),
    path('password-reset/',PasswordResetView.as_view(template_name='accounts/registration/password_reset.html',email_template_name='accounts/password_reset_email.html',success_url='/password_reset_done/'),name='password_reset'),
    path('password_reset_done/',PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/',PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html',post_reset_login=True,success_url='/password_reset_complete'),name='password_reset_confirm'),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'),name='password_reset_complete'),
    path('change_password/',PasswordChangeView.as_view(template_name='accounts/registration/password_change_view.html',success_url='/password_change_done'),name='password_change'),
    path('password_change_done/',PasswordChangeDoneView.as_view(template_name='accounts/registration/password_change_done.html'),name='password_change_done'),

    #User Profile and Dashboard Page

    path('profile/',views.dashboard,name='dashboard'),
    path('edit-profile/',views.edit_profile,name='edit_details'),
    path('address/',views.address,name='address'),
    path('add_address/',views.add_address,name='add_address'),
    path('edit-address/<slug:address_id>/',views.edit_address,name='edit_address'),
    path('delete-address/<slug:address_id>/',views.delete_address,name='delete_address'),
    path('setdefault/<slug:address_id>/',views.set_default,name='set_default'),

    #Set city
    path('get_city/',views.get_city,name='get_city'),
    
    
    
] 
