from django.core.exceptions import ValidationError
from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from .import models
import json
from django.http import HttpResponseForbidden
from django.conf import settings
from django.utils import timezone
import zoneinfo
from rest_framework import permissions
# from django.db import models as dj_models  
import logging
logger = logging.getLogger(__name__)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.exceptions import ValidationError

from datetime import datetime
from django.utils import timezone




def get_choice_field_value(obj, field_name):
    """
    A utility function that returns both the key and the display value for a ChoiceField.
    
    Parameters:
    - obj: The model instance containing the field.
    - field_name: The name of the field to retrieve the key and display value for.
    
    Returns:
    A dictionary with 'key' and 'value' (the display name).
    """
    field_value = getattr(obj, field_name)
    display_value = getattr(obj, f'get_{field_name}_display')()
    
    return {
        'key': field_value,
        'value': display_value
    }













def have_perm_fun(user, permission_names, require_all=True):
    """
    Check if the user has the specified permissions in the AppPermission model.
    
    :param user: The user object to check permissions for.
    :param permission_names: A list of permission names to check (e.g., ['appointments_create_perm', 'appointments_delete_perm']).
    :param require_all: If True, all permissions must be granted. If False, any single permission is sufficient.
    :return: True if the user has the required permissions, False otherwise.
    """  

    try:
        # Get the AppPermission object for the user
        clinic_permission = models.AppPermission.objects.get(user=user)
        
        # Check permissions based on the require_all flag
        if require_all:
            # All permissions must be True
            is_have_perm =all(getattr(clinic_permission, perm, False) for perm in permission_names)

            return is_have_perm
        else:
            # Any single permission can be True
            is_have_perm = any(getattr(clinic_permission, perm, False) for perm in permission_names)
    
            return is_have_perm
    
    except ObjectDoesNotExist:
        # If the user does not have a AppPermission record, return False
        return False




def validate_permission(user, permission_names, require_all=True):
    """
    Validates if a user has the required permissions.
    Raises appropriate exceptions if the user is not authenticated or lacks permission.
    
    :param user: Django User instance
    :param permission_names: List of permission field names (as strings)
    :param require_all: Whether all permissions are required or any one is sufficient
    :raises NotAuthenticated: if user is not logged in
    :raises PermissionDenied: if user lacks required permissions
    """
    if not user or not user.is_authenticated:
        raise NotAuthenticated("Login required.")
    
    if not have_perm_fun(user, permission_names, require_all):
        raise PermissionDenied("You do not have permission to access this resource.")


def is_role_admin_fun(user):
    is_admin  = False
    """
    Check if the user is admin or normal employee

    """

    
    if not user.is_authenticated:
        return   redirect('login')
    if user.user_role == 'admin' :
        is_admin =True
    return  is_admin





def is_role_admin(view_func):
    """
    Decorator to restrict access to users who must have the 'admin' role.
    If the user is not an admin, redirect them to the 403 page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user's role is 'admin'

        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.user_role != 'admin':
            return redirect('403')  # Redirect to a 403 page if not admin

        return view_func(request, *args, **kwargs)
    return _wrapped_view



class IsRoleAdminClass(permissions.BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False  # Unauthenticated users get 401
        return request.user.user_role == 'admin'


class IsRoleManagerClass(permissions.BasePermission):
    """
    Allows access only to users with the 'manager' or admin role.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False  # Unauthenticated users get 401
        return request.user.user_role  in ['manager' ,'admin'] # to giv admin manager previlige as well
   
   
   
   
   
   
   


# class HasCustomPermissions(permissions.BasePermission):
#     """
#     Custom DRF permission class to check if a user has specified permissions.

#     Args:
#         permission_list: List of permission field names.
#         require_all: All permissions required if True, otherwise any one.
#     """
#     def __init__(self, permission_list: list[str], require_all: bool = True):
#         self.permission_list = permission_list
#         self.require_all = require_all

#     def has_permission(self, request, view) -> bool:
#         if not request.user or not request.user.is_authenticated:
#             return False
#         return have_perm_fun(request.user, self.permission_list, self.require_all)
   
   
   