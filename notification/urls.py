from django.urls import path
from . import views 

app_name = 'notification'

urlpatterns = [
    path('notification-all/',views.notification_list,name='notification_list'),
    path('notification/<slug:notification_id>/',views.retrieve_notification,name='retrieve_notification'),
    path('notification/<slug:notification_id>/',views.delete_notification,name='delete_notification'),
    path('mark-all-read/',views.mark_all_read,name='mark_all_read'),

]
