from django.urls import path
from . import views

app_name= 'seller'

urlpatterns = [
    path('seller/registrations/',views.seller_registration,name='seller_reg'),
    path('dashboard/',views.seller_dashboard,name='seller_dashboard'),
]
