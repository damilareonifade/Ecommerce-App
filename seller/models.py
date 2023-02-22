from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()


class Shop(models.Model):
    name = models.CharField(verbose_name=('Shop Name'),max_length=450,null=True,blank=True)
    seller = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(verbose_name=('Shop Address'),max_length=1000,blank=True)

    
    class Meta:
        ordering = ('-name',)
    
    def __str__(self):
        return self.seller.name


@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        if instance.is_seller:
            Shop.objects.create(seller=instance)