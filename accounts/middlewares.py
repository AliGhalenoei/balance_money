from django.shortcuts import redirect
from django.urls import reverse


auth_paths = [
    reverse('login'),
    reverse('register'),
    reverse('password_reset'),
    reverse('password_reset_done'),
]

class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in auth_paths or request.path.startswith('/accounts/password/reset/confirm/'):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('login')
        
        return self.get_response(request)    



