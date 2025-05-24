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
from . import models
from django.db.models import ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .custom_user import CustomUser
from django.http import JsonResponse
from django.db import DatabaseError

##################

from .export.database_exports import export_model_to_excel ,export_many2many_to_excel


from .all_views.governorates_view import governorates_list_page  ,governorates_create_page ,governorates_delete_page ,governorates_form_page


from .all_views.centers_view import centers_list_page  ,centers_create_page ,centers_delete_page ,centers_form_page

from .all_views.service_providers_view import service_provider_list_page   ,service_provider_create_page ,service_provider_delete_page ,service_provider_form_page


from .all_views.affiliates_view import affiliates_list_page ,affiliates_create_page ,affiliates_delete_page ,affiliates_form_page 



from .all_views.branches_view import  branches_create_page ,branches_form_page ,branches_delete_page ,branches_list_page


from .all_views.main_activity_view import   main_activity_create_page ,main_activity_delete_page ,main_activity_form_page,main_activity_list_page


from .all_views.activity_type_view import  activity_types_create_page,activity_types_delete_page,activity_types_form_page,activity_types_list_page

from .all_views.activity_items_view import   activity_items_create_page ,activity_items_delete_page,activity_items_form_page,activity_items_list_page

from .all_views.main_survey_sections_view import  main_survey_sections_create_page ,main_survey_sections_delete_page ,main_survey_sections_form_page ,main_survey_sections_list_page 


from .all_views.sub_survey_sections_view import  sub_survey_sections_create_page ,sub_survey_sections_delete_page ,sub_survey_sections_form_page ,sub_survey_sections_list_page  



from .all_views.question_bank_view import question_bank_create_page,question_bank_delete_page,question_bank_form_page,question_bank_list_page


from .all_views.survey_view import  survey_create_page ,survey_delete_page ,survey_form_page ,survey_list_page ,add_questions ,calc_questions_res



from .all_views.all_reports_view import all_reports_view ,survey_reports_view ,get_survey_report_data


from .all_views.attchments import delete_attchment_file


from .getters_setters import   get_activity_type_from_main_activity  , update_state,get_service_provider_from_affiliate , get_need_center_from_affiliate  ,get_entity_type_from_affiliate ,get_survey_res_data

from .view_domain import main_activity_entity_type_domain ,get_main_activity_entity_type_activity_type_domain ,main_survey_sections_entity_type_domain ,affiliate_service_provider_domain ,entity_type_origin_type_survey_domain ,get_main_activity_origin_type_activity_type_domain ,main_activity_origin_type_domain ,get_survey_activity_item_domain ,get_survey_main_survey_sections_domain ,get_survey_supporting_activity_item_domain ,get_supporting_main_survey_sections_domain

from .all_views.home_page_view import  home_page


from .all_views.activity_items_geo import  activity_items_geo ,get_activity_items_geo_report



from .all_views.users_view import  users_list_page ,user_form_page ,users_create_page , users_delete_page








def not_found_page(request,exception=None):
    return render(request, '404.html')

def forbidden_page(request,exception=None):
    return render(request, '403.html')

def custom_500_view(request):
    return render(request, '500.html')

def custom_400_view(request,exception=None):
    return render(request, '400.html')
