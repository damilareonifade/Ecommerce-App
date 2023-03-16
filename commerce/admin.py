from django.contrib import admin
from .models import * 

admin.site.register((Category,ProductAttribute,ProductAttributeValue,ProductTypeAttribute,Stock,Brand,ProductAttributeValues,ProductImage,ProductType,Reviews,IpAddress))

## Include inline stacke

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class StockInline(admin.TabularInline):
    model = Stock

class ProductAdmin(admin.ModelAdmin):
    inlines = [StockInline,ProductImageInline,]
    
admin.site.register(Product,ProductAdmin)