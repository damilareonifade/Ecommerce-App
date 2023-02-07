from django.db import models
from mptt.models import TreeForeignKey,MPTTModel,TreeManyToManyField
from django.contrib.auth import get_user_model
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify



User = get_user_model()

def category_upload_path(instance,filename):
    return "category/icon/{}/{}".format(instance.name,filename)


def product_upload_path(instance,filename):
    return "product/icon/{}/{}".format(instance.product_image,filename)

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract= True


class Category(MPTTModel):
    name = models.CharField(verbose_name='Category Name',max_length=250,unique=True)
    icon = models.ImageField(upload_to=category_upload_path)
    parent = TreeForeignKey("self", null=True, blank=True, related_name="children",on_delete=models.CASCADE)
    slug= models.SlugField(max_length=250,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ["name"]


    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

class Product(TimeStampedModel):
    uuid =models.UUIDField(default=uuid.uuid4, editable=False)
    category = models.ManyToManyField(Category,related_name='category_product')
    name = models.CharField(verbose_name='Product Name',max_length=250,null=False,blank=False)
    seller = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    brand = models.ForeignKey("Brand",on_delete=models.CASCADE,related_name='product_brand')
    product_type = models.ForeignKey("ProductType",on_delete=models.CASCADE,related_name='product_type')
    attribute_values = models.ManyToManyField("ProductAttributeValue",related_name="product_attribute_values",through="ProductAttributeValues")
    product_description = models.TextField()
    product_excerpt = models.CharField(max_length=500,null=True,blank=True,verbose_name=_('Product Short Description'))
    weight = models.FloatField(unique=False,null=False,blank=False,verbose_name=_("product weight"))
    views = models.IntegerField(default=0)
    saved_post = models.ManyToManyField(User,related_name='user_saved_post')
    price = models.DecimalField(decimal_places=2,default=0.00, max_digits=10, null=True, blank=True)
    discount_price = models.DecimalField(decimal_places=2,default=0.00, max_digits=10, null=True, blank=True)
    showed_price = models.DecimalField(decimal_places=2,default=0.00,max_digits=10, null=True, blank=True)
        

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def save(self,*args, **kwargs):
        is_new= self.pk is None
        if is_new:
            self.showed_price = self.price - self.discount_price
        super().save(*args, **kwargs)

        if not is_new:
            self.showed_price = self.price - self.discount_price
        super().save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.showed_price}"
    
class Stock(TimeStampedModel):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='product_stock')
    in_stock = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    sold_stock = models.IntegerField(default=0)

    def save(self,*args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.in_stock = self.total_stock - self.sold_stock
        super().save(*args, **kwargs)
        if not is_new:
            self.in_stock = self.total_stock - self.sold_stock
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.product.name } available stock is {self.in_stock}'

    


class ProductImage(TimeStampedModel):
    product_image = models.ForeignKey("Product",on_delete=models.CASCADE,related_name='product_image')
    image = models.ImageField(upload_to=product_upload_path,null=True,blank=True,default="images/default.png",)
    is_feature = models.BooleanField()
    alt_text = models.TextField(max_length=72,blank=True,null=True)

    def __str__(self):
        return f"{self.product_image.name} images"

class ProductType(TimeStampedModel):
    name = models.CharField(max_length=255,unique=True,null=False,blank=False,verbose_name=_("type of product"),help_text=_("format: required, unique, max-255"))
    product_type_attributes = models.ManyToManyField("ProductAttribute",related_name="product_type_attributes",through="ProductTypeAttribute")

    def __str__(self):
        return self.name


class ProductAttributeValues(models.Model):
    """
    Product attribute values link table
    """

    attributevalues = models.ForeignKey("ProductAttributeValue",related_name="attributevaluess",on_delete=models.PROTECT,)
    productinventory = models.ForeignKey(Product,related_name="productattributevaluess",on_delete=models.PROTECT,)

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)

class ProductAttributeValue(models.Model):
    """
    Product attribute value table
    """

    product_attribute = models.ForeignKey("ProductAttribute",related_name="product_attribute",on_delete=models.PROTECT)
    attribute_value = models.CharField(max_length=255,unique=False,null=False,blank=False,verbose_name=_("attribute value"),help_text=_("format: required, max-255"))


    def __str__(self):
        return self.attribute_value

class ProductAttribute(models.Model):
    name = models.CharField(max_length=255,unique=True,null=False,blank=False,verbose_name=_("product attribute name"),help_text=_("format: required, unique, max-255"))
    description = models.TextField(unique=False,null=False,blank=False,verbose_name=_("product attribute description"),help_text=_("format: required"))

    def __str__(self):
        return self.name

class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey("ProductAttribute",related_name="productattribute",on_delete=models.PROTECT)
    product_type = models.ForeignKey(ProductType,related_name="producttype",on_delete=models.PROTECT)

    class Meta:
        unique_together = (("product_attribute", "product_type"),)

class Brand(TimeStampedModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Reviews(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_review")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True,related_name='product_reviews')
    rating = models.SmallIntegerField(default=0)
    review = models.TextField()

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return f'{self.user} commented on {self.product}'
    

class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField()
    product_id = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)


# from django.core.exceptions import ValidationError

# class MyModel(models.Model):
#     ...
#     my_file = models.FileField()
#     ...

#     def clean(self):
#         super().clean()
#         if self.my_file:
#             if self.my_file.size > 2 * 1024 * 1024:
#                 raise ValidationError("File size should not exceed 2MB.")

# class MyForm(forms.ModelForm):
#     ...
#     class Meta:
#         model = MyModel
#         fields = ['my_file',...]

#     def clean_my_file(self):
#         data = self.cleaned_data['my_file']
#         if data:
#             if data.size > 2 * 1024 * 1024:
#                 raise forms.ValidationError("File size should not exceed 2MB.")
#         return data