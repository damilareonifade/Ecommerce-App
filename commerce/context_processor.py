from .models import Category

def category_list(request):
    return {"category":Category.objects.all()}