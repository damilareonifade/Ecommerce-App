from django.core.management import BaseCommand
from accounts.models import State
from .states_and_goverment import nigeria_states_lga


class Command(BaseCommand):
    def handle(self,**options):
        for state, lgas in nigeria_states_lga.items():
            # Create a new instance of the States model for this state
            state_instance = State.objects.create(name=state)
            
            # Loop over each local government area in this state
            for lga in lgas:
                # Create a new instance of the States model for this local government area
                lga_instance = State.objects.create(name=lga, parent=state_instance)



    