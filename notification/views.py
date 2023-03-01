from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Notification

@login_required
def notification_list(request):
    notification = Notification.objects.filter(user=request.user)

    return render(request,'notification/list.html',{'notification':notification})

@login_required
def retrieve_notification(request,notification_id):
    notification = get_object_or_404(Notification,id=notification_id,user=request.user)
    notification.status('read')
    notification.save()

    return render(request,'notification/detail.html',{"notification":notification})

@login_required
def delete_notification(request,notification_id):
    notification = get_object_or_404(Notification,id=notification_id,user=request.user)
    notification.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def mark_all_read(request):
    notification = Notification.objects.filter(user=request.user)
    for notification in notification:
        notification.status = 'read'
        notification.save()

    return redirect(request.META['HTTP_REFERER'])




