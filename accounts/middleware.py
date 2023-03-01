
class DashboardMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    
    def __call__(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_seller:
                request.session['dashboard'] = "seller"
            else:
                request.session['dasboard'] = 'normal'
        
        else:
            request.session.pop('dashboard', None)
        
        response = self.get_response(request)
        return response

        