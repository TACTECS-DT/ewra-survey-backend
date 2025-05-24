from ..custom_user import CustomUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from django.conf import settings
from django.db.models import ProtectedError



class AppPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="المستخدم")

#   priamry access , will change letter 
    survey_access= models.BooleanField(verbose_name =" صلاحية الاستبيان")
    settings_access= models.BooleanField(verbose_name =" صلاحية الاعدادات")



    def __str__(self):
        return self.user.username



