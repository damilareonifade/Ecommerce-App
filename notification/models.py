from django.db import models
from accounts.models import CustomUser
from commerce.models import TimeStampedModel


class Notification(TimeStampedModel):
    status = (('read','Read'),('unread','Unread'))
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_notification')
    title = models.CharField(max_length=250)
    message = models.CharField(max_length=1000,null=True,blank=True)
    status = models.CharField(max_length=1000,choices=status,default='unread')


    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user} has notification {self.message}"