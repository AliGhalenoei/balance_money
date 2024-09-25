from django.shortcuts import redirect
from django.urls import resolve


class NotFoundMiddleware:

    def __init__(self , get_response):
        self.get_response = get_response

    def __call__(self , request):
        try:
            resolve(request.path)

        except:
            return redirect('404')
        
        response = self.get_response(request)
        return response

