
from django.shortcuts import render ,redirect ,get_object_or_404
from ..models import Attachment  
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.decorators import permission_required , login_required
from ..utils import is_role_admin  ,validate_permission
from ..all_models import main as base_models 
from ..all_models import survey as survey_models  
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def delete_attchment_file(request, file_id):
    if request.method == 'POST':
        file = get_object_or_404(Attachment, id=file_id)
        
        # Delete the file from the filesystem
        file.file.delete(save=False)
        
        # Delete the file record from the database
        file.delete()
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        raise ValidationError("Invalid request method")
    
    