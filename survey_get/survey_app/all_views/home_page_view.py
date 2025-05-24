from django.views.decorators.http import require_http_methods
from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.decorators import permission_required , login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from functools import wraps
from django.http import Http404
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from ..utils import is_role_admin_fun
from django.db.models import ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..custom_user import CustomUser
from django.http import JsonResponse
from django.db import DatabaseError
from ..all_models import main as main_models ,survey as survey_model



@login_required
def home_page(request):
    context ={}
    context["activity_items_n"] = main_models.ActivityItem.objects.count()
    if not is_role_admin_fun(request.user):
        return redirect("survey-list")
    return render(request, 'index.html',context=context)


