from commerce.models import Category,Product,Brand,ProductType,Product
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(id=1)
from faker import Faker
brand = Brand.objects.get(id=1)
type = ProductType.objects.get(id=1)
category = Category.objects.get(id=48)
def generate_dummy_data():
    faker = Faker()
    for i in range(1000):
        
        product = Product.objects.create(
            name=faker.name(),
            seller = user,
            product_description=faker.text(),
            weight=faker.random_int(),
            brand= brand,
            product_type=type,
            views=faker.random_int(),
            price=faker.random_int(),
            discount_price=faker.random_int(),
            
        )
        product.category.add(category)





