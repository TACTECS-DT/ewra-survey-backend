# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, permissions, pagination
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator
from django.http import Http404
from ...models import Affiliate 
from ...utils import IsRoleAdminClass , IsRoleManagerClass ,validate_permission ,get_choice_field_value  
from django.conf import settings
# from django.core.exceptions import ValidationError  #### dont usee this at all
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.core.exceptions import FieldError
from ... import  serializers  as all_serializers



class AffiliateGETAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
   
    allowed_methods = ['GET']


    
    def get(self, request):
    
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end
        
        # select related and prefitch related to optimize query
        records = Affiliate.objects.select_related("service_provider").all()

        #  filtering
        title_filter = request.query_params.get('name')
        if title_filter:
            records = records.filter(name__icontains=title_filter)

        # Pagination
        paginator = pagination.PageNumberPagination()
        paginator.page_size = settings.RECORD_PER_PAGE
        paginated_records = paginator.paginate_queryset(records, request)

        if paginated_records is None:
            raise NotFound("No records found or invalid pagination.")

        serializer = all_serializers.Affiliate_FORM_GET_Serializer(paginated_records, many=True)
        return paginator.get_paginated_response(serializer.data)


