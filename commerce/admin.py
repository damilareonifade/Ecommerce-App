from django.contrib import admin
from .models import * 

admin.site.register((Category,ProductAttribute,ProductAttributeValue,ProductTypeAttribute,Stock,Brand,ProductAttributeValues,ProductImage,ProductType,Reviews,IpAddress))

## Include inline stacke

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    
admin.site.register(Product,ProductAdmin)