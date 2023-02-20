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
    
    def add(self,product,product_qty):
        product_id= str(product.id)
        if product_id in self.basket:
            self.basket['product_id']['qty'] = product_qty
        
        else:
            self.basket[product_id] = {'price':str(product.price),'qty':str(product_qty)}
        
        self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in = product_ids)

        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * int(item['qty'])
            yield item
    
    def __len__(self):
        return sum(int(item["qty"]) for item in self.basket.values())
    
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * int(item['qty']) for item in self.basket.values())
    
    def get_total_price(self):
        pass


    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()
    
    def delete(self,product):
        del self.basket[product.id]
        self.save()
    

    def clear(self):
        # Remove basket from session
        del self.session[settings.CART_ID]
        self.save()
    
    def save(self):
        self.session.modified = True


