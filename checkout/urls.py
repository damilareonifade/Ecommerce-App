from django.urls import path
from . import views

app_name='checkout'

urlpatterns = [
    path('delivery-choices/',views.deliverychoices,name='checkout'),
    path('checkout/',views.checkout,name='deliver_option'),
    path('update_delivery_address/',views.basket_update_delivery,name='basket_update_delivery'),
]
