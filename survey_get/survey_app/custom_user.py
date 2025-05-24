from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

TIMEZONE_CHOICES = [
    ("Africa/Cairo", "تلقائى"),  # auto
    ("Etc/GMT-2", "  شتوى (+2)"),  # UTC+2 (Eastern European Time - EET)
    ("Etc/GMT-3", " صيفى (+3) " ),  # UTC+3 (Eastern European Summer Time - EEST)
]

class CustomUser(AbstractUser):

    login_state = models.CharField(max_length=200,verbose_name="الحالة", choices=[("active","نشط"),("inactive","غير نشط")], default="active")
   
    user_role = models.CharField(max_length=200,verbose_name="نوع المستخدم", choices=[("user","موظف"),("manager","مدير"),("admin","ادمن")], default="user")

    user_custom_timezone = models.CharField(max_length=200, choices=TIMEZONE_CHOICES, default='Africa/Cairo',verbose_name="التوقيت")

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return "Unnamed"