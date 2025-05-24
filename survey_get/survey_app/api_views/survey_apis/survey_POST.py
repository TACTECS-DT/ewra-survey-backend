from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, permissions, pagination
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator
from django.http import Http404
from ...utils import IsRoleAdminClass , IsRoleManagerClass ,validate_permission
from ... import serializers as all_serializers
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ... import models as all_models



class SurveyPOSTAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
    allowed_methods = ['POST']



    def post(self, request):
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end


        serializer = all_serializers.Survey_PATCH_POST_Serializer(data=request.data)
        
        # Check if the name already exists in the database
        name_value = request.data.get('name').strip()
        if all_models.Survey.objects.filter(name=name_value).exists():
            raise ValidationError(f"The name '{name_value}' already exists. Please choose a unique name.")
           
           
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
            
        response_serializer = all_serializers.Survey_FORM_GET_Serializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
