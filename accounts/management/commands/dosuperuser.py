from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    
    def handle(self,**options):
        user = User.objects.filter(email='taken@gmail.com')
        if not user:
            User.objects.create_superuser(email="taken@gmail.com",name="admin",password='takentaken')
