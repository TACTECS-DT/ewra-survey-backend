# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, permissions, pagination
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator
from django.http import Http404
from ...models import Governorate
from ...utils import IsRoleAdminClass , IsRoleManagerClass ,validate_permission
from django.conf import settings
# from django.core.exceptions import ValidationError  #### dont usee this at all
from rest_framework.exceptions import ValidationError

from django.db import IntegrityError

from django.db.models import ProtectedError
from.test_GET_api_view import  TestGETAPIView 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class TestPATCHGETAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
    allowed_methods = ['PATCH',"GET"]


    
    
    class GovernorateUpdateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255,required=True)
        longitude = serializers.CharField(max_length=255)
        latitude = serializers.CharField(max_length=255)
        #  add only wanted fileds to prevent mass assaignment 

        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

       

        def update(self, instance, validated_data):
            # add fields that want to updte here also 
            instance.name = validated_data.get('name', instance.name)
            instance.longitude = validated_data.get('longitude', instance.longitude)
            instance.latitude = validated_data.get('latitude', instance.latitude)
            instance.save()
            return instance



    def patch(self, request, pk=None):
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end


        try:
            if not pk:
                # this will not trigger my custom handeler
                # return Response({"error": "ID is required for update."}, status=status.       HTTP_400_BAD_REQUEST)
                # this will  trigger my custom handeler
                raise ValidationError(f"ID is required for update.")
            instance = Governorate.objects.get(pk=pk)
            
        except Governorate.DoesNotExist:
            raise ValidationError(f"Governorate with ID {pk} does not exist.")
        
        serializer = self.GovernorateUpdateSerializer(instance, data=request.data, partial=True)
        
        # Check if the name is being updated and if it already exists in the database
        if 'name' in request.data:
            name_value = request.data.get('name')
            if Governorate.objects.filter(name=name_value).exclude(pk=pk).exists():
                raise ValidationError(f"The name '{name_value}' already exists. Please choose a unique name.")

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        response_serializer = TestGETAPIView.GovernorateGETSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    
    
    
    
    
    
    
    def get(self, request, pk=None):
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end

        
        try:
            if not pk:
                # this will not trigger my custom handeler
                # return Response({"error": "ID is required for update."}, status=status.       HTTP_400_BAD_REQUEST)
                # this will  trigger my custom handeler
                raise ValidationError(f"ID is required for update.")
            record = Governorate.objects.get(pk=pk)
            
        except Governorate.DoesNotExist:
            raise ValidationError(f"Governorate with ID {pk} does not exist.")

        response_serializer = TestGETAPIView.GovernorateGETSerializer(record)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

