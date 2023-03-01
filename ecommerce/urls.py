
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls', namespace='accounts')),
    path('cart/',include('cart.urls',namespace = "basket")),
    path('',include("commerce.urls",namespace='commerce')),
    path('seller/',include('seller.urls',namespace='seller')),
    path('checkout/',include('checkout.urls',namespace='checkout')),
    path('notification/',include('notification.urls',namespace='notification')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
