from django.shortcuts import render
from django.http import JsonResponse
from . import models as base_models
from django.contrib.auth.decorators import permission_required , login_required
from django.http import JsonResponse






@login_required
def get_supporting_main_survey_sections_domain(request):
    main_activity = request.GET.get('main_activity')
    origin_type = request.GET.get('origin_type')

    if main_activity and origin_type:
        survey_sections = base_models.MainSurveySection.objects.filter(
            main_activity_id=main_activity,
            entity_type=origin_type
        ).values('id', 'name')
        return JsonResponse(list(survey_sections), safe=False)

    return JsonResponse([], safe=False)




@login_required
def get_survey_supporting_activity_item_domain(request):
    origin_type = request.GET.get('origin_type')
    main_activity = request.GET.get('main_activity')
    affiliate_id = request.GET.get('affiliate_id')

    if origin_type and main_activity and affiliate_id:
        activity_items = base_models.ActivityItem.objects.filter(
            entity_type=origin_type,
            main_activity_id=main_activity,
            affiliate_id=affiliate_id
        ).values('id', 'name')
        return JsonResponse(list(activity_items), safe=False)

    return JsonResponse([], safe=False)



@login_required
def get_survey_main_survey_sections_domain(request):
    origin_type = request.GET.get('origin_type')
    activity_type = request.GET.get('activity_type')

    if origin_type and activity_type:
        survey_sections = base_models.MainSurveySection.objects.filter(
            activity_type_id=activity_type,
            entity_type=origin_type
        ).values('id', 'name')
        return JsonResponse(list(survey_sections), safe=False)

    return JsonResponse([], safe=False)






@login_required
def get_survey_activity_item_domain(request):
    origin_type = request.GET.get('origin_type')
    activity_type = request.GET.get('activity_type')
    affiliate_id = request.GET.get('affiliate_id')

    if origin_type and activity_type and affiliate_id:
        activity_items = base_models.ActivityItem.objects.filter(
            entity_type=origin_type,
            activity_type_id=activity_type,
            affiliate_id=affiliate_id
        ).values('id', 'name')
        return JsonResponse(list(activity_items), safe=False)

    return JsonResponse([], safe=False)













@login_required
def affiliate_service_provider_domain(request):
    service_provider = request.GET.get('service_provider', None)
    if service_provider:
        affiliates = base_models.Affiliate.objects.filter(service_provider=service_provider).values('id', 'name')
        return JsonResponse(list(affiliates), safe=False)
    return JsonResponse([], safe=False)


@login_required
def main_activity_entity_type_domain(request):
    entity_type = request.GET.get('entity_type', None)
    if entity_type:
        activities = base_models.MainActivity.objects.filter(entity_type=entity_type).values('id', 'name')
        return JsonResponse(list(activities), safe=False)
    return JsonResponse([], safe=False)


@login_required
def entity_type_origin_type_survey_domain(request):
    origin_type = request.GET.get('origin_type', None)
    if origin_type:
        activities = base_models.MainActivity.objects.filter(entity_type=origin_type).values('id', 'name')
        return JsonResponse(list(activities), safe=False)
    return JsonResponse([], safe=False)



@login_required
def get_main_activity_origin_type_activity_type_domain(request):

    main_activity = request.GET.get('main_activity')
    origin_type = request.GET.get('origin_type')
    if main_activity and origin_type:
        activity_types = base_models.ActivityType.objects.filter(
            main_activity_id=main_activity,
            entity_type=origin_type
        ).values('id', 'name')
        return JsonResponse(list(activity_types), safe=False)
    return JsonResponse([], safe=False)


@login_required
def main_activity_origin_type_domain(request):
    origin_type = request.GET.get('origin_type', None)
    if origin_type:
        activities = base_models.MainActivity.objects.filter(entity_type=origin_type).values('id', 'name')
        return JsonResponse(list(activities), safe=False)
    return JsonResponse([], safe=False)






@login_required
def get_main_activity_entity_type_activity_type_domain(request):
    """
    Returns activity types filtered by main_activity and entity_type.
    This simulates the domain: [("main_activity", "=", main_activity), ("entity_type", "=", entity_type)]
    """
    main_activity = request.GET.get('main_activity')
    entity_type = request.GET.get('entity_type')
    if main_activity and entity_type:
        activity_types = base_models.ActivityType.objects.filter(
            main_activity_id=main_activity,
            entity_type=entity_type
        ).values('id', 'name')
        return JsonResponse(list(activity_types), safe=False)
    return JsonResponse([], safe=False)




@login_required
def main_survey_sections_entity_type_domain(request):
    entity_type = request.GET.get('entity_type', None)
    if entity_type:
        activities = base_models.MainSurveySection.objects.filter(entity_type=entity_type).values('id', 'name')
        return JsonResponse(list(activities), safe=False)
    return JsonResponse([], safe=False)

