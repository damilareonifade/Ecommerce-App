from django.urls import path
from . import views

app_name='checkout'

urlpatterns = [
    path('checkout/',views.deliverychoices,name='checkout'),
    path('update_delivery_address/',views.basket_update_delivery,name='basket_update_delivery'),
]
