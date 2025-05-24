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

class TestPOSTAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
    allowed_methods = ['POST']


    
    
    class GovernorateCreateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255,required=True)

        #  add only wanted fileds to prevent mass assaignment (whewre user can set(inject) dissalwed filed vlaue  with allwed once)

# automaticly called with is_valid from serialzer obj and must follow validate_<field_name>
# in this case name is requerd already from database level so its not do more here but will be useful at  optinal field that must be requerid  under certin condtions 

        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

       


# to map create with  creation model 
        def create(self, validated_data):
            return Governorate.objects.create(**validated_data)





    def post(self, request):
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end


        serializer = self.GovernorateCreateSerializer(data=request.data)
        
        # Check if the name already exists in the database
        name_value = request.data.get('name').strip()
        if Governorate.objects.filter(name=name_value).exists():
            raise ValidationError(f"The name '{name_value}' already exists. Please choose a unique name.")
           
           
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
            
        response_serializer = TestGETAPIView.GovernorateGETSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
