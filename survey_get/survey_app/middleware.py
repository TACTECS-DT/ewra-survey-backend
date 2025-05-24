import logging
from django.shortcuts import render ,redirect ,get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
import zoneinfo
from django.utils import timezone

from django.conf import settings

logger = logging.getLogger('django')





 
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in ["/login/"]:
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
       
        
        
        










class ExceptionLoggingMiddleware:
    """
    Middleware to log exceptions automatically without adding try/except in views.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Proceed with request handling
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"An unhandled error occurred: {str(e)}", exc_info=True)
            from django.conf import settings
            from django.urls import reverse

            if settings.DEBUG:
                raise e
            else:
                return render(reverse('custom_500_view'))      
        return response





class CheckLoginStateMiddleware:
    """
    Middleware to check if the user's login_state is 'inactive' after each request.
    If it's inactive, log the user out and show a message.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if the user has been deactivated
            if request.user.login_state == 'inactive':
                messages.error(request, "تم الغاء تنشيط حسابك الرجاء التواصل مع احد المشرفين")
                logout(request)
                return redirect('login')
        
        response = self.get_response(request)
        return response



class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_timezone = request.user.user_custom_timezone
            timezone.activate(zoneinfo.ZoneInfo(user_timezone))
        else:
            timezone.deactivate()
        return self.get_response(request)