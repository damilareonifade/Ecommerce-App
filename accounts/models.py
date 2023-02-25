from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from mptt.models import TreeForeignKey,MPTTModel
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email Field Is Required')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('name','admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff True")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser as True")
        
        return self.create_user(email,password,**extra_fields)
        


Role = (('Admin','admin'),('Sales rep','Sales rep'),('customer','customer'))


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name=_("Email"), max_length=254,unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=80,)
    role = models.CharField(max_length=10,choices=Role,default='customer')
    phone_number =models.CharField(max_length=342,null=True,blank=True,unique=True)
    country = models.CharField(max_length=234,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff= models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance).save()
    
    
        


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name=_("User Field"), on_delete=models.CASCADE)
    profile_pics = models.ImageField(upload_to='media',null=True,blank=True)
    dob= models.DateField(null=True,blank=True)
    address = models.ForeignKey("AddressGlobal",related_name='user_address',null=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.user.name


class AddressGlobal(models.Model):
    # id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    address = models.TextField()
    city = models.CharField(max_length=250)
    state = models.ForeignKey("State",null=True,blank=True,on_delete=models.CASCADE,related_name='address_state')
    country = models.CharField(max_length=100,default='Nigeria')
    phone_number = models.CharField(max_length=250,null=True,blank=True)
    is_default = models.BooleanField(default=False)
    price = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.city

class State(MPTTModel):
    name = models.CharField(max_length=72)
    parent = TreeForeignKey("self", null=True, blank=True, related_name="children",on_delete=models.CASCADE)
    price = models.CharField(max_length=250,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser,related_name='custom_user',null=True,on_delete=models.SET_NULL)
    email = models.EmailField()
    full_name = models.CharField(max_length=50)
    option = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"{self.full_name} {self.option}"
    
def create_user_activity(user,option):
    UserActivity.objects.create(user=user,email=user.email,full_name=user.name,option=option)

