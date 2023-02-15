from django.urls import path,include
from . import views 

urlpatterns = [
    path("basket/add/",views.basket_add,name='basket_add'),
]
