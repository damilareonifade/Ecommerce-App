from django.shortcuts import render,get_object_or_404
from .models import *
from django.db.models import Count,Aggregate,Max,Sum
from django.core.cache import cache
from .forms import CommentForm
import json
from django.http import JsonResponse

def homepage(request):
    products = Product.objects.select_related('seller', 'brand', 'product_type').annotate(highest_views=Max('views')).order_by('-highest_views')
    top_categories = Category.objects.filter(category_product__id__in = products).annotate(num_products=Count('category_product')).order_by('-num_products')[:5]
    trendy_product = Product.objects.select_related('seller','brand','product_type').annotate(highest_view=Max('views')).order_by('highest_view')[:10]
    latest_arrival = Product.objects.order_by("-created_at")[:12]

    return render(request,'store/index.html',{"category":top_categories,'trendy_product':trendy_product,"latest_arrival":latest_arrival})

def product_detail(request,slug):
    product = Product.objects.get(uuid=slug)
    product_count = product.product_reviews.count()
    product.views += 1
    product.save()
    reviews= Reviews.objects.all()

    if request.POST.get('action')  == 'post':
        comment = str(request.POST.get('comment'))
        rating = int(request.POST.get('rating'))
        Reviews.objects.create(user=request.user,product=product.id,review=comment,rating=rating)

        review =Reviews.objects.all()
        reviews= json.dumps(list(review))
        plan_obj = json.loads(reviews)
        response = JsonResponse({'reviews': plan_obj})
        return response

    if product_count <= 19:
        number_of_stars = range(1)
    elif product_count >=20 and product_count<= 30:
        number_of_stars = range(2)
    elif product_count >=31 and product_count<= 40:
        number_of_stars =range(3)
    elif product_count >=41 and product_count<= 50:
        number_of_stars = range(4)
    elif product_count >=51 and product_count<= 60:
        number_of_stars =range(5)
       
    
    return render(request,'store/detail.html',{'product':product,"number_of_stars":number_of_stars,'reviews':reviews})


def category_product(request,slug):
    categories = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=categories)

    return render(request,'store/all_categories.html',{"products":products})

def saved_post(request,slug):
    post = Product.objects.get(uuid=slug)
    pass
    
    