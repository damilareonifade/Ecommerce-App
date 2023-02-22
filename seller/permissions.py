from django.contrib.auth.decorators import user_passes_test


def seller(function):
    decorator = user_passes_test(lambda u: u.is_authenticated and u.is_seller,login_url='/accounts/login')
    return decorator(function)