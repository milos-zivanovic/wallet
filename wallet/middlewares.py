from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # List of URL names that can be accessed without authentication
        excluded_urls = [
            reverse('login'),
        ]

        # Check if the user is authenticated or if the request path is in excluded_urls
        if not request.user.is_authenticated and request.path not in excluded_urls:
            return redirect(settings.LOGIN_URL)
