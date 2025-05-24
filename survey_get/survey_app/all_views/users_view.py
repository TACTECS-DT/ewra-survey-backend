from django.views.decorators.http import require_http_methods
from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.decorators import permission_required , login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from functools import wraps
from django.http import Http404
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.db.models import ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..custom_user import CustomUser
from .. import forms 
from ..utils import is_role_admin 
from .. import utils
from django.conf import settings


@login_required
@is_role_admin
@require_http_methods(["GET"])
def users_list_page(request):
    fitched_records = CustomUser.objects.all().order_by("-id")
    
    # Pagination logic
    paginator = Paginator(fitched_records, settings.RECORD_PER_PAGE)  
    page = request.GET.get('page', 1)

    try:
        fitched_records_paginated = paginator.page(page)
    except PageNotAnInteger:
        fitched_records_paginated = paginator.page(1)
    except EmptyPage:
        fitched_records_paginated = paginator.page(paginator.num_pages)
    context = {
        "fitched_records": fitched_records_paginated,
    }
    return render(request, 'users/users_list.html', context)





@is_role_admin
@login_required
@require_http_methods(["GET","POST","PATCH","DELETE"])
def user_form_page(request,pk):
    if not pk :
        redirect('users-list')
    try:
        current_record = get_object_or_404(CustomUser, pk=pk)
        if not current_record : 
            return redirect("404")
    except Http404:
        return redirect('404')               


    if request.method == 'POST':

        form = forms.UserUpdateForm(request.POST, instance=current_record)
        if form.is_valid():
            form.save()  
            form.save_m2m()
            return redirect("users-list")  
                       
    else:
        form = forms.UserUpdateForm(instance=current_record)

    return render(request, 'users/users_form.html', {'form': form,"current_record":current_record})






@is_role_admin
@login_required
@require_http_methods(["POST","GET"])
def users_create_page(request):

    if request.method == 'POST':
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            return redirect('users-list')  
    else:
        form = forms.UserCreateForm()

    return render(request, 'users/users_create.html', {'form': form})








@is_role_admin
@require_http_methods(["POST","DELETE","GET"])
@login_required
def users_delete_page(request,pk):
    if not pk :
        return redirect('users-list')
    
    have_access= utils.is_role_admin_fun(request.user)
    try:
        user = get_object_or_404(CustomUser, pk=pk)
    except Http404:
        return redirect('404')               

    if have_access :
        try :
            user.delete()
            
        except ProtectedError as e:
            return render(request, 'ProtectedError.html', {
                'references': e.protected_objects,
            })
    
    if not have_access :
        return redirect('403')
    
    return redirect('users-list')

