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
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404


class SurveyDELETEAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated,IsRoleManagerClass]
    allowed_methods = ['DELETE']






    def delete(self, request):
        # Check user access to this operation from permission model
        validate_permission(request.user, ['settings_access', "survey_access"], require_all=True)

        # Get the list of IDs from the query parameter (comma-separated)
        ids_param = request.query_params.get('ids', None)

        if not ids_param:
            raise ValidationError("No Records provided for deletion.")

        # Split the comma-separated string into a list of IDs
        ids_to_delete = ids_param.split(',')

        try:
            # Convert to integers (assuming IDs are integers)
            ids_to_delete = [int(id) for id in ids_to_delete]
        except ValueError:
            raise ValidationError("Invalid ID format. All IDs must be integers.")

        # Initialize lists to track deleted and error records
        deleted_records = []
        error_records = []

        for id in ids_to_delete:
            
            
            
            try:
                # Try to get the instance
                instance = get_object_or_404(Survey, pk=id)
                
                if instance.state not in ["draft","in_progress"]:
                    raise  ValidationError("Cannot Delete Survey that not in  draft or in progress state ")
        
                instance.delete()
                deleted_records.append(id)  

            except Survey.DoesNotExist:
                error_records.append({"id": id, "error": "Record not found."})

            except ProtectedError:
                error_records.append({"id": id, "error": "Cannot delete. The record is related to other existing records."})

            except Exception as e:
                # If any other error happens, record the error and continue
                error_records.append({"id": id, "error": str(e)})

        # Prepare the response data
        response_data = {
            "deleted": deleted_records,
            "errors": error_records
        }
        # If all records were deleted, modify the response

        response_data['all_deleted'] = len(deleted_records) == len(ids_to_delete)
        
        # If there were any errors, include them in the response
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)





