
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse ,JsonResponse ,HttpResponseNotAllowed
from django.contrib.auth import logout
from django.contrib.auth.views import  LoginView 
from django.views.decorators.http import require_GET

# @require_GET
# def jwt_logout_page(request):
#     if request.method != "GET":
#         return HttpResponseNotAllowed(['GET'])
#     response = JsonResponse({"message": "Logged out successfully."})
    
#     # Overwrite the access token cookie
#     response.set_cookie(
#         key='access_token',
#         value='',
#         expires=0,
#         httponly=True,
#         secure=True,
#         samesite='Lax',
#         path='/'
#     )
    
#     # Overwrite the refresh token cookie (if you have one)
#     response.set_cookie(
#         key='refresh_token',
#         value='',
#         expires=0,
#         httponly=True,
#         secure=True,
#         samesite='Lax',
#         path='/'
#     )
    
#     return response



def logout_page(request):
    logout(request)
    return redirect('login') 




class CustomLoginView(LoginView):

    def form_valid(self, form):
        user = form.get_user()

  
        if user.login_state == 'inactive':
            messages.error(self.request, "تم الغاء تنشيط حسابك الرجاء التواصل مع احد المشرفين")
            return redirect('login')  

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "بيانات غير صحيحه")
        return super().form_invalid(form)

