from django.shortcuts import render
from django.http import JsonResponse
from . import models as base_models 
from .all_models.survey import  Survey 
from django.contrib.auth.decorators import permission_required , login_required
import json
from decimal import Decimal
from django.http import HttpResponse
from .utils import validate_permission
@login_required  
def update_state(request):
     # cheack user acsess to this operation from permission model
    validate_permission(request.user, ["survey_access"], require_all=True)
    # end
    manager_states =  ['confirmed','cancelled','draft']
    # admin_states =  ['draft']
    if request.method == "POST":
        user_role = request.user.user_role
        try:
            data = json.loads(request.body)
            survey_id = data.get("survey_id")
            new_state = data.get("new_state").strip()
            
            if new_state in manager_states  and user_role not in ['manager','admin']: 
                return  HttpResponse("You Have no access to do this action", status=403)
            
            # if new_state in admin_states  and user_role !='admin': 
            #     return  HttpResponse("You Have no access to do this action", status=403)
                
            # Get the survey record
            survey = Survey.objects.get(id=survey_id)
            survey.state = new_state
            survey.save()

            return JsonResponse({"success": True, "new_state": new_state})
        except Survey.DoesNotExist:
            return JsonResponse({"success": False, "error": "Survey not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



@login_required
def get_survey_res_data(request):
    survey_id = request.GET.get('survey_id')

    if survey_id:
        try:
            survey = Survey.objects.get(id=survey_id)
            data = {
                'full_mark': Decimal(survey.full_mark) if survey.full_mark else Decimal(0),
                'visit_result': Decimal(survey.visit_result) if survey.visit_result else Decimal(0),
                'visit_result_percntage': Decimal(survey.visit_result_percntage) if survey.visit_result_percntage else Decimal(0),
                'questions_added': survey.questions_added,
                'visit_result_done': survey.visit_result_done,
            }
            return JsonResponse(data)
        except Survey.DoesNotExist:
            return JsonResponse({'error': 'Survey not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
def get_activity_type_from_main_activity(request):
    main_activityId = request.GET.get('main_activityId')
    if main_activityId:
        rec = base_models.MainActivity.objects.filter(id=main_activityId).first()
        if rec and rec.activity_type:
            return JsonResponse({'activity_type_name': str(rec.get_activity_type_display())})
    
    return JsonResponse({})


@login_required
def get_need_center_from_affiliate(request):
    affiliate_id = request.GET.get('affiliate_id')
    if affiliate_id:
        affiliate = base_models.Affiliate.objects.filter(id=affiliate_id).first()
        if affiliate :
            return JsonResponse({'need_center': affiliate.need_center})
    
    return JsonResponse({})


@login_required
def get_entity_type_from_affiliate(request):
    affiliate_id = request.GET.get('affiliate_id')
    if affiliate_id:
        affiliate = base_models.Affiliate.objects.filter(id=affiliate_id).first()
        if affiliate :
            return JsonResponse({'entity_type': str(affiliate.get_entity_type_display())})
    
    return JsonResponse({})


@login_required
def get_service_provider_from_affiliate(request):
    affiliate_id = request.GET.get('affiliate_id')
    if affiliate_id:
        affiliate = base_models.Affiliate.objects.filter(id=affiliate_id).first()
        if affiliate and affiliate.service_provider :
            return JsonResponse({'service_provider': str(affiliate.service_provider)})
    
    return JsonResponse({})
