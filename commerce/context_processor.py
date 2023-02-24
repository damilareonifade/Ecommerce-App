from .models import Category,Product
from django.contrib.auth.decorators import login_required

def category_list(request):
    return {"category":Category.objects.all()}

def saved_post_count(request):
    product = 0
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.filter(saved_post=request.user).count()
    return {'product_number':product}