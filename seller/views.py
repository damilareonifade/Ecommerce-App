from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import permissions

@login_required
def seller_registration(request):
    pass