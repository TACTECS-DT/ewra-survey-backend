import os
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.decorators import permission_required , login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .import models


allowed_extensions =['jpg', 'jpeg', 'png', 'pdf', 'docx', 'xlsx', 'txt']
validate_file_type = FileExtensionValidator(allowed_extensions)



# File size validator
def validate_file_size(file):
    # Maximum file size in bytes (e.g., 5MB)
    max_file_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_file_size:
        raise ValidationError(f"The file size should not exceed {max_file_size / (1024 * 1024)} MB.")
