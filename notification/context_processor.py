from .models import Notification

def notification_list(request):
    return {"notification":Notification.objects.all()}