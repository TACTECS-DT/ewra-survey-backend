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
from django.core.exceptions import FieldError



class TestGETAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
    allowed_methods = ['GET']



# get
    class GovernorateGETSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        
        
        #custom or computed field -> its not found in Governorate module  : 
        # must defined with SerializerMethodField
        tax = serializers.SerializerMethodField(method_name="set_tax")
    
        def set_tax(self,governate):
            return governate.name +' hi'
        
    def get(self, request):
    
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end

        records = Governorate.objects.all()

        # Simple filtering
        title_filter = request.query_params.get('name')
        if title_filter:
            records = records.filter(name__icontains=title_filter)

        # Pagination
        paginator = pagination.PageNumberPagination()
        paginator.page_size = settings.RECORD_PER_PAGE
        paginated_records = paginator.paginate_queryset(records, request)

        if paginated_records is None:
            raise NotFound("No records found or invalid pagination.")

        serializer = self.GovernorateGETSerializer(paginated_records, many=True)
        return paginator.get_paginated_response(serializer.data)


