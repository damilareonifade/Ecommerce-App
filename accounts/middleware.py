
class DashboardMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    
    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_type = 'seller' if request.user.is_seller else 'normal'
            request.session.setdefault('dashboard', {})['user_type'] = user_type
        else:
            request.session.pop('dashboard', None)
        
        response = self.get_response(request)
        return response

        