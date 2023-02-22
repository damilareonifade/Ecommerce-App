from django.core.management import BaseCommand
from accounts.models import State


class Command(BaseCommand):
    def handle(self,**options):
        states = ['Lagos',"Ibadan",'Ogun',"Abia","Akwa-Ibom","Enugu","Dutse",'Kaduna']
        for i in states:
            State.objects.create(name=i,price='2000')



    