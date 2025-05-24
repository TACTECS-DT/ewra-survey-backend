# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, permissions, pagination
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator
from django.http import Http404
from ...models import Survey
from ...utils import IsRoleAdminClass , IsRoleManagerClass ,validate_permission
from ... import serializers as all_serializers
from django.conf import settings
# from django.core.exceptions import ValidationError  #### dont usee this at all
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware


                

class SurveyPATCHGETAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
    allowed_methods = ['PATCH',"GET"]



    def patch(self, request, pk=None):
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end

        try:
            if not pk:
                raise ValidationError(f"ID is required for update.")
            
            instance = Survey.objects.select_related('service_provider', 'affiliate', 'center', 'main_activity',  'activity_type',  'activity_item',   'supporting_activity_item').get(pk=pk)
                
        except Survey.DoesNotExist:
            raise ValidationError(f"Record with ID {pk} does not exist.")
        
        # state check
        if instance.state not in ["draft","in_progress"]:
            raise ValidationError("Cannot Change Survey that not in  draft or in progress state ")
        # end state check

        # race condition handleing
        # TODO
        #end race condition handleing
        
        
        serializer = all_serializers.Survey_PATCH_POST_Serializer(instance, data=request.data, partial=True)
        
        
        # Validation
        # Check if the name is being updated and if it already exists in the database
        if 'name' in request.data:
            name_value = request.data.get('name').strip()
            if Survey.objects.filter(name=name_value).exclude(pk=pk).exists():
                raise ValidationError(f"The name '{name_value}' already exists. Please choose a unique name.")

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()


         # date timezone validation
         #    Time zone from request and  +2 and +3 handleing 
        # TODO




        # questions update  handleing
        # TODO
        
        #   look to survey form to keep all steps in mind
        # important to do : 
            #     questions = SurveyQuestion.objects.filter(survey=current_record).select_related(
            # "survey", "question", "sub_survey_section", "main_survey_section"
            #     )
            #  question.last_updated = timezone.now()
            # question.last_updated_by = request.user
            # instance.last_updated = timezone.now()
        
        
        #end questions handleing
        



        response_serializer = all_serializers.Survey_FORM_GET_Serializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    
    
    def get(self, request, pk=None):
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end

        
        try:
            if not pk:
                # this will  trigger my custom handeler
                raise ValidationError(f"ID is required for update.")
            
            record = Survey.objects.select_related('service_provider', 'affiliate', 'center', 'main_activity',  'activity_type',  'activity_item',   'supporting_activity_item').get(pk=pk)
                    
        except Survey.DoesNotExist:
            raise ValidationError(f"Record with ID {pk} does not exist.")

        response_serializer = all_serializers.Survey_FORM_GET_Serializer(record)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
