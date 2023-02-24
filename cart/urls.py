from django.urls import path,include
from . import views 

app_name = 'cart'

urlpatterns = [
    path("basket/add/",views.basket_add,name='basket_add'),
    path('all/cart/',views.basket_all,name='basket_all'),
    path('basket/delete/',views.basket_delete,name='basket_delete'),
    path('basket/update/',views.basket_update,name='basket_update'),
    path('checkout/',views.checkout,name='checkout'),
]
