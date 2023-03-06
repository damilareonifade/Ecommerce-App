from django.urls import path 
from . import views

app_name='orders'

urlpatterns = [
    path('payment/check/',views.check_payment,name='check_payment'),
    path('payment/',views.make_payment,name='make_payment')

]
