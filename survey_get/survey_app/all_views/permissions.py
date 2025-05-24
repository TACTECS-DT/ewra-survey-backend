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
from .. import models
from django.db.models import ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..custom_user import CustomUser

from ..utils import is_role_admin 

from django.conf import settings
from django.http import JsonResponse


@login_required
@is_role_admin
@require_http_methods(["GET"])
def permessions_list_page(request):
 
 
    fitched_records = models.AppPermission.objects.all().order_by("-id")

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

    return render(request, 'permissions/permissions_list.html', context)









@is_role_admin
@login_required
@require_http_methods(["GET","POST","PATCH"])
def permissions_form_page(request, pk):
    try:
        current_record = get_object_or_404(models.AppPermission, pk=pk)
        if not current_record : 
            return redirect("404")
    except Http404:
        return redirect('404')               

    if request.method == 'POST':
        # Update the record with form data
        current_record.survey_access = request.POST.get('survey_access') == 'on'
        current_record.settings_access = request.POST.get('settings_access') == 'on'

        # Save the updated record
        current_record.save()
        return redirect('permissions-form',pk=current_record.pk)

    # Render the form with the current record
    return render(request, 'permissions/permessions_form.html', {'current_record': current_record})


@login_required
@is_role_admin
@require_http_methods(["POST"])
def check_and_create_permissions(request):
    users_without_permissions = []
    users = CustomUser.objects.all()

    for user in users:
        # Check if the user has a AppPermission record
        if not models.AppPermission.objects.filter(user=user).exists():
            # Create a AppPermission record for the user
            models.AppPermission.objects.create(user=user, **settings.USER_DEFAULT_PERMISSIONS)
            users_without_permissions.append(user.username)

    if users_without_permissions:
        message = f"تم انشاء صلاحيات ل  : {', '.join(users_without_permissions)}"
    else:
        message = "جميع المستخدمين لديهم صلاحيات بالفعل"

    return JsonResponse({"success": True, "message": message})