from collections import defaultdict
from django.shortcuts import render
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
from django.db.models import Avg
from django.db.models import ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..custom_user import CustomUser
from .. import forms 
from ..utils import is_role_admin 
from .. import utils
from ..all_models import main as base_models 
from ..all_models import survey as survey_models  
import json
from django.http import JsonResponse

@login_required
@is_role_admin
@require_http_methods(["GET"])
def activity_items_geo(request):
    
    context = { }

    return render(request, 'reports/activity_items_geo.html', context)




# @login_required
# @is_role_admin
# @require_http_methods(["GET"])
# def get_activity_items_geo_report(request):
#     activity_item_ids = base_models.ActivityItem.objects.values_list(['id'], flat=True)

#     surveys = survey_models.Survey.objects.filter(
#         activity_item__in=activity_item_ids
#     ) | survey_models.Survey.objects.filter(
#         supporting_activity_item__in=activity_item_ids
#     )

#     activity_items_map = defaultdict(list)

#     for survey in surveys:
#         activity_item = survey.activity_item if survey.activity_item.id in activity_item_ids else survey.supporting_activity_item
#         activity_items_map[activity_item.id].append({
#             "activity_item_lat": activity_item.latitude,
#             "activity_item_long": activity_item.longitude,
#             "survey_name": survey.name,
#             "visit_result": float(survey.visit_result) ,
#         "visit_result_percentage": float(survey.visit_result_percntage)  # Convert Decimal to float
#         })

#     activity_items_list = [
#         {
#             "id": key,
#             "latitude": items[0]["activity_item_lat"],
#             "longitude": items[0]["activity_item_long"],
#             "surveys": items,
#         }
    #     for key, items in activity_items_map.items()
    # ]

    # data = {
    #     "activity_items_json": json.dumps(activity_items_list)  
    # }

    # return      JsonResponse(data)  # Ensure Django sends a proper JSON response


@login_required
@require_http_methods(["GET"])
def get_activity_items_geo_report(request):

    activity_items = base_models.ActivityItem.objects.all()


    surveys = survey_models.Survey.objects.select_related("activity_item").all()


    activity_items_map = defaultdict(list)
    for survey in surveys:
        activity_items_map[survey.activity_item_id].append(survey)

    # Prepare response data
    activity_items_list = []
    for activity_item in activity_items:
        surveys_for_item = activity_items_map.get(activity_item.id, [])

        # Calculate average visit result
        avg_visit_result = (
            sum(survey.visit_result for survey in surveys_for_item) / len(surveys_for_item)
            if surveys_for_item else 0
        )
        average_result_percetange = (
            sum(survey.visit_result_percntage for survey in surveys_for_item) / len(surveys_for_item)
            if surveys_for_item else 0
        )

        # Structure activity item data
        activity_item_data = {
            "id": activity_item.id,
            "name": activity_item.name,
            "latitude": activity_item.latitude,
            "longitude": activity_item.longitude,
            "average_result": avg_visit_result,
            "average_result_percetange": average_result_percetange,
            "surveys": [
                {
                    "survey_id": survey.id,
                    "survey_name": survey.name,
                    "visit_result": float(survey.visit_result),
                    "visit_result_percentage": float(survey.visit_result_percntage),
                }
                for survey in surveys_for_item
            ],
        }

        activity_items_list.append(activity_item_data)

    return JsonResponse({"activity_items": activity_items_list})
