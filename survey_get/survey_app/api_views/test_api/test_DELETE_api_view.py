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


class TestDELETEAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
    allowed_methods = ['DELETE']



    def delete(self, request, pk=None):
        # cheack user acsess to this operation from permission model
        validate_permission(request.user, ['settings_access',"survey_access"], require_all=True)
        # end


        if not pk:
                # this will not trigger my custom handeler
                # return Response({"error": "ID is required for update."}, status=status.       HTTP_400_BAD_REQUEST)
                # this will  trigger my custom handeler
            raise ValidationError(f"ID is required for update.")
            
        instance = Governorate.objects.filter(pk=pk).first()
        if not instance:
            raise NotFound("Governorate not found.")

        try:
            instance.delete()
            return Response({"message": "Governorate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except ProtectedError:
            raise ValidationError("error : Cannot delete this Governorate. It is related to other protected objects.")



