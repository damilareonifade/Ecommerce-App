from django.conf import settings
from commerce.models import Product
from decimal import Decimal

class Basket():

    def __init__(self,request):
        self.session = request.session
        basket = self.session.get(settings.CART_ID)
        if settings.CART_ID not in self.session:
            basket = request.session[settings.CART_ID] ={}
        self.basket = basket
    
    def add(self,request,product,product_size,product_qty,product_color):
        product_id= str(self.product.id)
        if product_id in self.basket:
            self.basket['product_id']['qty'] = product_qty
        
        else:
            self.basket[product_id] = {'price':str(product.price),'qty':str(product_qty),'size':str(product_size),'color':str(product_color)}
        
        self.save()

    def __iter__(self,request):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in = product_ids)

        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
    
    def __len__(self,request):
        return sum(int(item["qty"]) for item in self.basket.values())
    
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def save(self):
        self.session.modified = True


