from django.conf import settings
from commerce.models import Product
from accounts.models import AddressGlobal
from checkout.models import DeliveryOptions
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
            self.basket[product_id]['qty'] = product_qty
        
        else:
            self.basket[product_id] = {'price':str(product.price),'qty':str(product_qty)}
        
        self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product


        for item in basket.values():
            item['price'] = item['price']
            item['total_price'] = Decimal(item['price']) * int(item['qty'])
            item['total_price']
            yield item
    
    def __len__(self):
        return sum(int(item["qty"]) for item in self.basket.values())
    
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * int(item['qty']) for item in self.basket.values())
    
    def basket_update_delivery(self, deliveryprice):
        subtotal = sum(Decimal(item['price']) * int(item['qty']) for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    
    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = AddressGlobal.objects.get(id=self.session["purchase"]["address_id"])
            delivery_price = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
            amount = int(newprice.state.price) + int(delivery_price)
            return amount

    def get_total_price(self):
        subtotal = sum(Decimal(item['price']) * int(item['qty']) for item in self.basket.values())
        if subtotal == 0:
            total = Decimal(0.00)
            return total            
        
        elif 'purchase' in self.session:
            location_price = AddressGlobal.objects.get(id=self.session["purchase"]["address_id"])
            shipping = int(location_price.state.price)
            total = subtotal + Decimal(shipping)        
            return total
        else:
            total = Decimal(0.00)
            return total
     


    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()
    
    def delete(self,product):        
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()
    

    def clear(self):
        # Remove basket from session
        del self.session[settings.CART_ID]
        self.save()
    
    def save(self):
        self.session.modified = True


