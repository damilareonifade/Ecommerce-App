from django.urls import path
from . import views

app_name = 'commerce'

urlpatterns = [
    path('',views.homepage,name="index"),
    path('product/<slug:slug>/',views.product_detail,name='details'),
    path('category/<slug:slug>/',views.category_product,name='category_product'),
    path('saved-post/<slug:slug>/',views.saved_post,name='saved_post'),
]
