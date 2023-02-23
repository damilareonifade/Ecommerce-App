from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model,login
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate


class PhoneNumberBackend(ModelBackend):

    def authenticate(self, request, username, password, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone_number=username,is_active=True)
        except UserModel.DoesNotExist:
            raise PermissionDenied("Invalid password Or Phone Number")
        
        if not user.check_password(password):
            raise authenticate.AuthenticationFailed("Invalid password")
        else:
            return user
