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
from ..utils import is_role_admin  ,validate_permission
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
from django.db.models import OuterRef, Subquery
from ..models import Attachment  
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Prefetch
@login_required
@require_http_methods(["GET"])
def survey_list_page(request):
    # cheack user acsess to this operation from permission model
    validate_permission(request.user, ["survey_access"], require_all=True)
    # end
    fitched_records = survey_models.Survey.objects.all().select_related(
        'service_provider', 'affiliate', 'center', 'main_activity',  'activity_type',  'activity_item',   'supporting_activity_item', 
    ).order_by("-id")

    # Pagination logic
    paginator = Paginator(fitched_records, settings.RECORD_PER_PAGE)  
    page = request.GET.get('page', 1)
    user_role = request.user.user_role
    is_admin = user_role =='admin'
    is_manager = user_role in['manager' ,'admin']
    try:
        fitched_records_paginated = paginator.page(page)
    except PageNotAnInteger:
        fitched_records_paginated = paginator.page(1)
    except EmptyPage:
        fitched_records_paginated = paginator.page(paginator.num_pages)
    
    context = {
        "fitched_records": fitched_records_paginated,
                'is_admin': is_admin,
        'is_manager': is_manager,
    }

    return render(request, 'survey/survey_list.html', context)




@login_required
@require_http_methods(["GET", "POST", "PATCH", "DELETE"])
def survey_form_page(request, pk):
    # cheack user acsess to this operation from permission model
    validate_permission(request.user, ["survey_access"], require_all=True)
    # end
    any_question_changed = False
    user_role = request.user.user_role
    is_admin = user_role =='admin'
    is_manager = user_role in['manager' ,'admin']

    if not pk:
        return redirect('survey-list')
    current_record = get_object_or_404(
        survey_models.Survey.objects.select_related(
            'service_provider', 'affiliate', 'center',
            'main_activity', 'activity_type', 'activity_item', 'supporting_activity_item'
            ),
        pk=pk
    )

    question_ct = ContentType.objects.get_for_model(SurveyQuestion)
    questions = SurveyQuestion.objects.filter(survey=current_record).select_related(
        "survey", "question", "sub_survey_section", "main_survey_section"
    ).prefetch_related(Prefetch(
        'attachments',  # This is the GenericRelation field on SurveyQuestion
        queryset=Attachment.objects.filter(content_type=question_ct),
        to_attr='prefetched_attachments'  # You can access this in the template
    ))



    if request.method == 'POST':
                    
        if current_record.state not in ["draft","in_progress"]:
                return  HttpResponse("Cannot Change Survey that not in  draft or in progress state ", status=400)
        
        
        request_last_refresh_time = request.POST.get("last_refresh_time")
        record_last_updated = current_record.last_updated

        if request_last_refresh_time:
            request_last_refresh_time_with_zt = datetime.fromisoformat(request_last_refresh_time).replace(tzinfo=dt_timezone.utc)

            if record_last_updated > request_last_refresh_time_with_zt:
                return HttpResponse("This survey has been updated by another user. Please refresh and try again.",status=400)
        form = forms.SurveyUpdateForm(request.POST, instance=current_record)
        
        if form.is_valid():
            if current_record.state  =='draft':
                form.save()
            for question in questions:
                
                
            # Handle multiple files
                attachment_field = f'attachments_{question.id}'
               
                
                
                if attachment_field in request.FILES:
                    uploaded_files = request.FILES.getlist(attachment_field)

                    for uploaded_file in uploaded_files:
                        # Create a new attachment for each uploaded file
                        Attachment.objects.create(
                            file=uploaded_file,
                            uploaded_by=request.user,
                            content_type=ContentType.objects.get_for_model(SurveyQuestion),
                            object_id=question.id,
                            # related_reference=f"SurveyQuestion #{question.id}",
                            description="Uploaded attachment for survey question"
                        )

                #end attachmens
                
                
                
                
                new_notes = request.POST.get(f'notes_{question.id}', "").strip()
                new_answer_recommendations = request.POST.get(f'recommendations_{question.id}', "").strip()
                new_percentage = request.POST.get(f'percentage_{question.id}', "0.00000000000000000000").strip()
                if new_percentage == "NA":
                    new_percentage_decimal = None  # Store NULL for N/A
                
                else :
                    try:
                        new_percentage_decimal = Decimal(new_percentage)
                    except:
                        new_percentage_decimal = Decimal(0)

       
               


                # Check if any field has changed
                if (question.answer_notes != new_notes or question.answer_percentage != new_percentage_decimal or question.answer_recommendations != new_answer_recommendations):
  
                    question.answer_notes = new_notes
                    question.answer_recommendations = new_answer_recommendations
                    question.answer_percentage = new_percentage_decimal
         
                    
                    if question.last_updated_by is None and (not question.answer_recommendations  and not question.answer_notes and question.answer_percentage == 0.00000000000000000000):
                        # If this is the first ever answer (from initial state), keep last_updated_by as None
                        question.last_updated_by = None
                    else:
                        # If someone is updating an already-answered question, set to current user
                        question.last_updated = timezone.now()
                        question.last_updated_by = request.user
                                    
                                    
                    question.save()

                    any_question_changed = True  
            # If any question was updated, update last_updated on survey
            if any_question_changed:
                current_record.last_updated = timezone.now()
                current_record.visit_result_done = False
                current_record.save(update_fields=["last_updated","visit_result_done"])
            messages.success(request, "Survey and modified questions saved successfully.")
            return redirect('survey-form', pk=current_record.pk)

    else:
        form = forms.SurveyUpdateForm(instance=current_record)


    return render(request, 'survey/survey_form.html', {
        'form': form,
        'is_admin': is_admin,
        'is_manager': is_manager,
            "record_state": {
        "code" : current_record.state , 
        "name" : current_record.get_state_display() , 
        },
        "current_record": current_record,
        "questions": questions,
            "allowed_states": ['draft', 'in_progress'],  
            "is_allowed_state" : current_record.state in ['draft', 'in_progress'],
    })



@login_required
@require_http_methods(["POST","GET"])
def survey_create_page(request):
    # cheack user acsess to this operation from permission model
    validate_permission(request.user, ["survey_access"], require_all=True)
    # end
    if request.method == 'POST':
        form = forms.SurveyCreateForm(request.POST)
        if form.is_valid():
            # rec = form.save(commit=False)
            # rec.save()
            try:
                    rec = form.save()
                    return redirect("survey-form",rec.pk)
            except ValidationError as e:
                    # If there's a validation error, display it to the user
                    for error in e.messages:
                        messages.error(request, error)
        else:
                messages.error(request, "There was an error with the form submission.")     
            
    else:
        form = forms.SurveyCreateForm()

    return render(request, 'survey/survey_create.html', {'form': form})




@require_http_methods(["POST","DELETE","GET"])
@login_required
@is_role_admin
def survey_delete_page(request,pk):
    # cheack user acsess to this operation from permission model
    validate_permission(request.user, ["survey_access"], require_all=True)
    # end
    if not pk :
        return redirect('survey-list')
    
    have_access= utils.is_role_admin_fun(request.user)
    try:
        rec = get_object_or_404(survey_models.Survey, pk=pk)
    except Http404:
        return redirect('404')         
          
    # if rec.state not in ["draft"]:
    #         return  HttpResponse("Cannot Delete Survey that not in  draft state ", status=400)
        
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
    
    return redirect('survey-list')






@login_required
def add_questions(request):
    # cheack user acsess to this operation from permission model
    validate_permission(request.user, ["survey_access"], require_all=True)
    # end
 
    if request.method == "POST":

        try:
            data = json.loads(request.body)
            survey_id = data.get("survey_id")
            if not survey_id:
                return JsonResponse({"success": False, "error": "ID not set"}, status=400)
            
            survey = Survey.objects.get(id=survey_id)
            if survey.state not in ["draft"]:
                return  HttpResponse("Cannot change Survey that not in  draft  state ", status=400)
        
 
            main_activity = survey.main_activity.id
            activity_type = survey.activity_type.id
            entity_type = survey.origin_type
            
            if not main_activity:
                return JsonResponse({"success": False, "error": "اضف   النشاط اولا"}, status=400)
                        
            if not activity_type:
                return JsonResponse({"success": False, "error": "اضف نوع النشاط  اولا"}, status=400)
            
            if not entity_type:
                return JsonResponse({"success": False, "error": "اضف   نوع الأصل اولا"}, status=400)
            
            
            
            # Clear existing questions
            SurveyQuestion.objects.filter(survey=survey).delete()
            
            main_survey_sections = base_models.MainSurveySection.objects.filter(main_activity=main_activity ,activity_type=activity_type,entity_type=entity_type)
            
            sub_survey_sections = base_models.SubSurveySection.objects.filter(main_survey_sections__in=main_survey_sections)
    
       
       
            
            for section in sub_survey_sections:

                questions = QuestionBank.objects.filter(sub_survey_sections__in=[section], is_active=True)

                for question in questions:

                    SurveyQuestion.objects.create(
                                survey=survey,
                                question=question,
                                sub_survey_section=section,
                                main_survey_section=section.main_survey_sections,
                                kpi=question.kpi,
                                answer_percentage=0.00000000000000000000,
                                  last_updated_by=None,
                                  last_updated=None,
                            )
                            
            # Update survey metadata
            survey.questions_added = True
            survey.visit_result_done = False
            survey.visit_result = 0.00000000000000000000
            survey.visit_result_percntage = 0.00000000000000000000
            survey.save()
            
            # end 
            return JsonResponse({"success": True})
        except Survey.DoesNotExist:
            return JsonResponse({"success": False, "error": "Survey not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


@login_required
def calc_questions_res(request):
    # cheack user acsess to this operation from permission model
    validate_permission(request.user, ["survey_access"], require_all=True)
    # end
    user_role = request.user.user_role
    is_admin = user_role =='admin'
    is_manager = user_role in['manager' ,'admin']

    if request.method == "POST":
        if not is_admin and not is_manager:
            return  HttpResponse("You have no access to do this action ", status=403)
        
        try:
            data = json.loads(request.body)
            survey_id = data.get("survey_id")

            if not survey_id:
                return JsonResponse({"success": False, "error": "Survey ID not provided"}, status=400)

            survey = Survey.objects.get(id=survey_id)

            if survey.state != 'confirmed':
                return HttpResponse("Cannot calculate result for a survey that is not in the confirmed state", status=400)

            # Fetch all related survey questions
            survey_questions = SurveyQuestion.objects.filter(survey=survey, answer_percentage__isnull=False)
            # remove NA questions
            if not survey_questions.exists():
                return JsonResponse({"success": False, "error": "No questions found for this survey"}, status=400)
            
            total_kpi = Decimal(0)
            total_sub_kpi = Decimal(0)

            with transaction.atomic():  # Ensures atomicity of database updates
                for question in survey_questions:
                    # Use Decimal to avoid floating-point errors
                    line_kpi = question.kpi or Decimal(0)
                    line_answer_percentage = question.answer_percentage or Decimal(0)

                    line_kpi_sub=(line_kpi * line_answer_percentage).quantize(Decimal('0.00000000000000000000'))

                    question.kpi_sub_total = line_kpi_sub


                    total_sub_kpi += line_kpi_sub
                    total_kpi += line_kpi
    

                # Bulk update to optimize database writes
                SurveyQuestion.objects.bulk_update(survey_questions, ['kpi_sub_total'])

                # Update survey results
                survey.visit_result = total_sub_kpi
                survey.visit_result_percntage = total_sub_kpi / total_kpi if total_kpi != 0 else Decimal(0) #to avoid devision by 0

                survey.visit_result_done = True
                survey.full_mark = total_kpi
                survey.save()

            return JsonResponse({"success": True, "message": "Survey results calculated successfully"})

        except Survey.DoesNotExist:
            return JsonResponse({"success": False, "error": "Survey not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


def delete_attchment_file(file_ids):
    for file_id in file_ids :
        file = get_object_or_404(models.LicenseFile, id=file_id)
        # Delete the file from the filesystem
        file.file.delete(save=False)
        # Delete the file record from the database
        file.delete()
