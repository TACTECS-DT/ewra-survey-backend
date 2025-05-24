from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from django.conf import settings
from django.db import models as djmodels
from django.contrib.auth.admin import GroupAdmin
from django.utils.translation import gettext as _

@admin.register(models.CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'user_role', 'login_state',"first_name", "last_name")
   
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "user_role",
                    "login_state",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","user_role","login_state"),
            },
        ),
    )
