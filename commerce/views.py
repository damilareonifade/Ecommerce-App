from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,HttpResponse
from .models import *
from django.db.models import Count,Aggregate,Max,Sum
from django.core.cache import cache
from .forms import CommentForm
import json
from django.contrib.postgres.search import SearchQuery,SearchVector,SearchRank
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

#5ADD23B7

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
    reviews= Reviews.objects.filter(product=product)
    
    #code to get the product attribute of the product here
    product_att_name = Product.objects.filter(uuid=slug).values('attribute_values__product_attribute__name').exclude(attribute_values__product_attribute__name=None).distinct()
    attribute_dict = {}
    for attr_name in product_att_name:
        data = attr_name['attribute_values__product_attribute__name']
        attribute_values = ProductAttributeValue.objects.filter(product_attribute__name=data).prefetch_related('attributevaluess')
        for attr_value in attribute_values:
            product_count = attr_value.attributevaluess.count()
            attribute_dict.setdefault(data, []).append({'attribute_value': attr_value.attribute_value})


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
       
    
    return render(request,'store/detail.html',{'product':product,"number_of_stars":number_of_stars,'reviews':reviews,'attribute_dict':attribute_dict})

def review_create(request,slug):
    try:
        product = Product.objects.get(uuid=slug)

    except Exception as e:
        return e

    if request.method  == 'POST':
        comment = str(request.POST.get('message',None))
        
        record, created = Reviews.objects.get_or_create(user=request.user,product=product,review=comment)
        if not created:
            record.review = comment
            record.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])



def category_product(request,slug):
    categories = Category.objects.prefetch_related('category_product').get(slug=slug)

    product_att_name = categories.category_product.values('attribute_values__product_attribute__name').exclude(attribute_values__product_attribute__name=None).distinct()
    attribute_dict = {}
    for attr_name in product_att_name:
        data = attr_name['attribute_values__product_attribute__name']
        attribute_values = ProductAttributeValue.objects.filter(product_attribute__name=data).prefetch_related('attributevaluess').distinct()
        for attr_value in attribute_values:
            product_count = attr_value.attributevaluess.count()
            attribute_dict.setdefault(data, []).append({'attribute_value': attr_value.attribute_value, 'product_count': product_count})
    
    #search functionality
    if 'search_product' in request.GET:
        search = request.GET.get('search_product',None)
        query= SearchQuery(search)
        vector = SearchVector("name",weight='A')+ SearchVector("product_description",weight='A') + SearchVector('brand',weight='B') + SearchVector('seller',weight='C')
        products = categories.category_product.annotate(rank=SearchRank(vector,query)).order_by("-rank",)
    
    elif 'latest' in request.GET:
        products = categories.category_product.all().order_by('-created_at',)
    
    elif 'popularity' in request.GET:
        products = categories.category_product.all().order_by('-views',)
    else:
        products = categories.category_product.all()
       
    paginator = Paginator(products,20)
    try:
        page = request.GET.get("page")
        objects = paginator.get_page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request,'store/category_list.html',{"categories":categories,'objects':objects,"product_count":product_count,'attribute_dict':attribute_dict})

def saved_post(request,slug):
    product = Product.objects.get(uuid=slug)
    if product.saved_post.filter(id =request.user.id).exists():
        product.saved_post.remove(request.user)
    else:
        product.saved_post.add(request.user)
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def all_saved_product(request):
    product = Product.objects.filter(saved_post=request.user)
    return render(request,'store/all_saved_product.html',{'product':product})


def product_search(request):
    try:
        if 'search' in request.GET:
            search = request.GET.get("search",None)
            query = SearchQuery(search)
            product = Product.objects.annotate(search=SearchVector('sku','name','product_description','seller','category','brand')).filter(search=query)
            
            paginator = Paginator(product,20)
            try:
                page = request.GET.get("page")
                objects = paginator.get_page(page)
            except PageNotAnInteger:
                objects = paginator.page(1)
            except EmptyPage:
                objects = paginator.page(paginator.num_pages)
    except:
        objects ='There is no product or brand with such name'

    return render(request,'store/product_search.html',{'objects':objects})

def category_ajax_view(request,slug):
    categories = Category.objects.get(slug=slug)
    if request.GET.get('action') == 'post':
        values = request.GET.get('values',None)
        product = categories.category_product.filter(attribute_values__attribute_value=values).distinct()
        paginator = Paginator(product,20)
        try:
            page = request.GET.get("page")
            objects = paginator.get_page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        product_list = list(product.values('id',"uuid",'name', 'price','showed_price'))
        response = JsonResponse({'objects':product_list})
        return response
    return HttpResponse("here are we")