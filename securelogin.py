from django.conf import settings
from django.contrib.auth import get_user
from django.shortcuts import redirect
from django.urls import reverse





class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and active
        user = get_user(request)
        if user.is_authenticated and not user.is_active:
            return redirect('welcome')

        return response



class DisableBackButtonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        else:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        return response

    def process_request(self, request):
        if not request.user.is_authenticated and request.method == 'GET':
            request.session['last_request'] = request.path

    def process_response(self, request, response):
        if request.path == '/' and 'last_request' in request.session:
            del request.session['last_request']
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return None
        if 'last_request' in request.session:
            if request.path != '/' and request.path != request.session['last_request']:
                del request.session['last_request']
                return redirect('home')
        return None


