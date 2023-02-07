from django.urls import path
from . import views

app_name = 'commerce'

urlpatterns = [
    path('',views.homepage,name="index"),
    path('product/<slug:slug>/',views.product_detail,name='details'),
    path('review/<slug:slug>/',views.review_create,name='review_create'),
    path('category/<slug:slug>/',views.category_product,name='category_product'),
    path('saved-post/<slug:slug>/',views.saved_post,name='saved_post'),
    path('all-saved-product/',views.all_saved_product,name='all_saved_product'),
]
