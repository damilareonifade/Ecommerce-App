from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import *
from django.db.models import Count,Aggregate,Max,Sum
from django.core.cache import cache
from .forms import CommentForm
import json
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def homepage(request):
    products = Product.objects.select_related('seller', 'brand', 'product_type').annotate(highest_views=Max('views')).order_by('-highest_views')
    top_categories = Category.objects.filter(category_product__id__in = products).annotate(num_products=Count('category_product')).order_by('-num_products')[:5]
    trendy_product = Product.objects.select_related('seller','brand','product_type').annotate(highest_view=Max('views')).order_by('highest_view')[:10]
    latest_arrival = Product.objects.order_by("-created_at")[:12]

    return render(request,'store/index.html',{"category":top_categories,'trendy_product':trendy_product,"latest_arrival":latest_arrival})

def product_detail(request,slug):
    product = Product.objects.get(uuid=slug)
    product_count = product.product_reviews.count()
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    review,created = IpAddress.objects.get_or_create(ip_address=ip,product_id=product)
    if created:
        product.views += 1
        product.save()

    reviews= Reviews.objects.all()

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

def review_create(request,slug):
    product = Product.objects.get(uuid=slug)
    if request.GET.get('action')  == 'post':
        comment = str(request.GET.get('comment',None))
        rating = str(request.GET.get('rating',None))
        print(comment)
        print(rating)
        
        record, created = Reviews.objects.get_or_create(user=request.user,product=product.id,review=comment,rating=rating)
        if not created:
            record.review = comment
            record.rating = rating
            record.save()

        review =Reviews.objects.all()
        reviews= json.dumps(list(review))
        plan_obj = json.loads(reviews)
        response = JsonResponse({'reviews': plan_obj})
        return response


def category_product(request,slug):
    categories = Category.objects.prefetch_related('category_product').get(slug=slug)
    products = categories.category_product.all()
    paginator = Paginator(products,5)
    try:
        page = request.GET.get("page")
        objects = paginator.get_page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request,'store/category_list.html',{"categories":categories,'objects':objects})

def saved_post(request,slug):
    product = Product.objects.get(uuid=slug)
    if product.saved_post.filter(id =request.user.id).exists():
        product.saved_post.remove(request.user)
    else:
        product.saved_post.add(request.user)
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
