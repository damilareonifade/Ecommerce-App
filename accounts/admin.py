from django.contrib import admin
from .models import * 

admin.site.register((CustomUser,UserActivity,UserProfile,AddressGlobal,State))