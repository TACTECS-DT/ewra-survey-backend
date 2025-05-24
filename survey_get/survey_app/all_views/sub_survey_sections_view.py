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
from django.conf import settings

from django.db.models import ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..custom_user import CustomUser
from .. import forms 
from ..utils import is_role_admin 
from .. import utils
from ..all_models import main as base_models 
from ..all_models import survey as survey_models  



@login_required
@is_role_admin
@require_http_methods(["GET"])
def sub_survey_sections_list_page(request):
    fitched_records = base_models.SubSurveySection.objects.select_related("main_survey_sections").all().order_by("-id")

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

    return render(request, 'sub_survey_sections/sub_survey_sections_list.html', context)


@login_required
@is_role_admin
@require_http_methods(["GET","POST","PATCH","DELETE"])
def sub_survey_sections_form_page(request,pk):
    if not pk :
        redirect('sub-survey-sections-list')
    try:
        current_record = get_object_or_404(base_models.SubSurveySection, pk=pk)
        if not current_record : 
            return redirect("404")
    except Http404:
        return redirect('404')               


    if request.method == 'POST':

        form = forms.SubSurveySectionUpdateForm(request.POST, instance=current_record)
        if form.is_valid():
            form.save()  
            return redirect("sub-survey-sections-list")  
                       
    else:
        form = forms.SubSurveySectionUpdateForm(instance=current_record)

    return render(request, 'sub_survey_sections/sub_survey_sections_form.html', {'form': form,"current_record":current_record})



@login_required
@is_role_admin
@require_http_methods(["POST","GET"])
def sub_survey_sections_create_page(request):

    if request.method == 'POST':
        form = forms.SubSurveySectionCreateForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.save()
            return redirect('sub-survey-sections-list')  
    else:
        form = forms.SubSurveySectionCreateForm()

    return render(request, 'sub_survey_sections/sub_survey_sections_create.html', {'form': form})




@require_http_methods(["POST","DELETE","GET"])
@login_required
@is_role_admin
def sub_survey_sections_delete_page(request,pk):
    if not pk :
        return redirect('sub-survey-sections-list')
    
    have_access= utils.is_role_admin_fun(request.user)
    try:
        rec = get_object_or_404(base_models.SubSurveySection, pk=pk)
    except Http404:
        return redirect('404')               

    if have_access :
        try :
            rec.delete()
            
        except ProtectedError as e:
            return render(request, 'ProtectedError.html', {
                'references': e.protected_objects,
            })
    

    if not have_access :
        exception = 'not allwed'
        return redirect('403',exception)
    
    return redirect('sub-survey-sections-list')
