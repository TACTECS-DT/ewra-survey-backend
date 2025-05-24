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
from django.forms import modelformset_factory
from django.db.models import ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..custom_user import CustomUser
from .. import forms 
from ..utils import is_role_admin 
from .. import utils
from ..all_models import main as base_models 
from ..all_models import survey as survey_models  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Survey, SubSurveySection, QuestionBank, SurveyQuestion
import json
from django.http import HttpResponse
from django.utils import timezone
import datetime
from datetime import datetime, timezone as dt_timezone
from decimal import Decimal
from django.db import transaction
from collections import defaultdict
from decimal import Decimal
from django.db.models import Sum


@login_required
@is_role_admin
@require_http_methods(["GET"])
def all_reports_view(request):

    return render(request, 'reports/all_reports.html')


@login_required
@is_role_admin
@require_http_methods(["GET"])
def survey_reports_view(request):
    valid_surveys = survey_models.Survey.objects.select_related(
        'service_provider', 'affiliate', 'center', 'main_activity',  'activity_type',  'activity_item',   'supporting_activity_item',  
    ).filter(state='confirmed')
    
    context = {
        "valid_surveys" : valid_surveys
    }
    return render(request, 'reports/survey_reports.html',context)



@login_required
@is_role_admin
@require_http_methods(["GET"])
def get_survey_report_data(request):
    if request.method == "GET":
        total_main_full_mark = Decimal("0.00000000000000000000")
        total_main_percentage = Decimal("0.00000000000000000000")
        total_main_total = Decimal("0.00000000000000000000")
        average_main_percentage = Decimal("0.00000000000000000000") 
        
        try:
            survey_id = request.GET.get("survey_id")
            reports_data = {}
 
            survey = Survey.objects.get(id=int(survey_id))
         
            survey_questions = SurveyQuestion.objects.filter(survey=survey, answer_percentage__isnull=False)
   
            
            if not survey_questions.exists():
                return JsonResponse({"success": False, "error": "No questions found for this survey"}, status=400)

            main_section_data = defaultdict(lambda: {
                "sub_sections": defaultdict(lambda: {
                    "questions": [],
                    "sub_total": Decimal("0.00000000000000000000"),
                "sub_full_mark": Decimal("0.00000000000000000000"),
                "sub_percentage": Decimal("0.00000000000000000000"),
                    
                    
                }),
                "main_total": Decimal("0.00000000000000000000"),
                "main_full_mark": Decimal("0.00000000000000000000"),
                "main_percentage": Decimal("0.00000000000000000000")
                
            })
            
            for question in survey_questions:
                main = question.main_survey_section
                sub = question.sub_survey_section

                main_section_data[main]["sub_sections"][sub]["questions"].append({
                    "question": question.question.name,  
                    "kpi_sub_total": float(question.kpi_sub_total or 0),
                    "answer_percentage": float(question.answer_percentage or 0),
                    # "is_NA": "true" if  question.answer_percentage is None else "false",
                    "kpi": float(question.kpi or 0),
                    "answer_notes": question.answer_notes,
                    "answer_recommendations": question.answer_recommendations,
                    
                })

                # Sum kpis  for sub section
                main_section_data[main]["sub_sections"][sub]["sub_total"] += question.kpi_sub_total or Decimal("0.00000000000000000000")
                
                main_section_data[main]["sub_sections"][sub]["sub_full_mark"] += question.kpi or Decimal("0.00000000000000000000")
    
        #  compute main totals from sub_totals
            for main_section, data in main_section_data.items():
                for sub_section_data in data["sub_sections"].values():
                    data["main_total"] += sub_section_data["sub_total"]
                    data["main_full_mark"] += sub_section_data["sub_full_mark"]
                    
                    # Compute sub_percentage
                    if sub_section_data["sub_full_mark"] > 0:
                        sub_section_data["sub_percentage"] = (sub_section_data["sub_total"] / sub_section_data["sub_full_mark"]) * 100

                # Compute main_percentage
                if data["main_full_mark"] > 0:
                    data["main_percentage"] = (data["main_total"] / data["main_full_mark"]) * 100
          
            # Prepare final structure
            reports_data = {
                str(main_section): {
                    "main_total": float(data["main_total"]),
                    "main_full_mark": float(data["main_full_mark"]),
                        "main_percentage": float(data["main_percentage"]),
                    "sub_sections": {
                        str(sub_section): {
                            "sub_total": float(sub_data["sub_total"]),
                            "sub_full_mark": float(sub_data["sub_full_mark"]),
                            "sub_percentage": float(sub_data["sub_percentage"]),
                            "questions": sub_data["questions"]
                        }
                        for sub_section, sub_data in data["sub_sections"].items()
                    }
                }
                for main_section, data in main_section_data.items()
            }
            
            
            for data in main_section_data.values():
                total_main_full_mark += data["main_full_mark"]
                total_main_percentage += data["main_percentage"]
                total_main_total += data["main_total"]
                
                
            main_section_count = len(main_section_data)     
            if main_section_count > 0:
                average_main_percentage = total_main_percentage / main_section_count  
                

                
            average_total_main_total_percentage =   ( total_main_total /total_main_full_mark ) *100
            
            return JsonResponse({"success": True, "reports_data":reports_data,"average_main_percentage" :average_main_percentage ,"total_main_total":total_main_total ,"average_total_main_total_percentage":average_total_main_total_percentage ,"total_main_full_mark":total_main_full_mark})
        
        
        except Survey.DoesNotExist:
            return JsonResponse({"success": False, "error": "Survey not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

