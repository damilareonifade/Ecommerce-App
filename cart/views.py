from django.shortcuts import render

def basket_add(request):
    if request.POST.get('action') == 'post':
        