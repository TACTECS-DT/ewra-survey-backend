from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import ProtectedError
# reletd_filed fo related 
from decimal import Decimal
from django.utils.html import escape
from .attachment import Attachment  


class Governorate(models.Model):
    name = models.CharField(max_length=255,verbose_name="المحافظة")
    latitude = models.CharField(verbose_name="خط العرض لمركز المدينة (Lat) ",null=True,max_length=500,blank=True)
    longitude = models.CharField(verbose_name="خط الطول لمركز المدينة (Long)",max_length=500,null=True,blank=True)
    def __str__(self):
        return self.name
    
    
    
    # prevent XSS attackes 
    fields_to_escape = ['name', 'latitude',"longitude"]
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        
        
class Center(models.Model):
    name = models.CharField(max_length=255,verbose_name="اسم المنطقة او المركز")
    governorate = models.ForeignKey('Governorate', on_delete=models.PROTECT,verbose_name="المحافظة")

    def __str__(self):
        return self.name


    
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        



class ServiceProvider(models.Model):
    name = models.CharField(max_length=255,verbose_name="اسم مقدم الخدمة")

    def __str__(self):
        return self.name

    
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        

class Affiliate(models.Model):
    name = models.CharField(max_length=255,verbose_name="اسم الجهة التابعة")
    entity_type = models.CharField(max_length=500,verbose_name="نوع الخدمة الخاصة بالجهة التابعة؟", choices=[('water','مياه شرب'),('sewage','صرف'),('both','مياه شرب وصرف')],null=True,blank=True)
    service_provider = models.ForeignKey('ServiceProvider',verbose_name='مقدم الخدمة', on_delete=models.PROTECT,null=True,blank=True)

    need_center = models.BooleanField(verbose_name ="يجب إضافة منطقه او مركز ؟ ")


    def __str__(self):
        return self.name
      
    
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        



class Branch(models.Model):
    name = models.CharField(max_length=255,verbose_name="اسم الفرع")

    affiliate = models.ForeignKey('Affiliate',verbose_name='الجهة التابعة', on_delete=models.PROTECT)

    # reletd_filed service_provider reletd with affiliate.service_provider with text 'مقدم الخدمة'


    def __str__(self):
        return self.name
      
       
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        

class MainActivity(models.Model):
    name = models.CharField(max_length=255,verbose_name="اسم النشاط")

    entity_type = models.CharField(max_length=500,verbose_name="نوع الاصل", choices=[('water','مياه شرب'),('sewage','صرف')],null=True)

    activity_type = models.CharField(max_length=500,verbose_name='رئيسى / داعم ', choices=[('main','رئيسى'),('supporter','داعم'),],null=True)

    def __str__(self):
        return self.name


       
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        

class ActivityType(models.Model):
    name = models.CharField(max_length=255,verbose_name='اسم نوع النشاط')

    entity_type = models.CharField(max_length=500,verbose_name="نوع الاصل", choices=[('water','مياه شرب'),('sewage','صرف')],null=True,blank=True)

    main_activity = models.ForeignKey('MainActivity',verbose_name='النشاط الرئيسى / داعم', on_delete=models.PROTECT,null=True,blank=True)
    #main_activity  domain='[("entity_type","=",entity_type)]


    # reletd_filed activity_type relted with main_activity.activity_type with string 'رئيسى / داعم '

    def __str__(self):
        return self.name
    
   
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        
  
class ActivityItem(models.Model):
    name = models.CharField(max_length=255,verbose_name='اسم الموقع ')

    entity_type = models.CharField(max_length=500,verbose_name="نوع الاصل", choices=[('water','مياه شرب'),('sewage','صرف')],null=True,blank=True)
    latitude = models.CharField(verbose_name="خط العرض (Lat)",null=True,max_length=500,blank=True)
    longitude = models.CharField(verbose_name=" خط الطول (Long)",max_length=500,null=True,blank=True)
   

    main_activity = models.ForeignKey('MainActivity',verbose_name='النشاط الرئيسى / داعم', on_delete=models.PROTECT,null=True,blank=True)
    #main_activity  domain='[("entity_type","=",entity_type)]


    activity_type = models.ForeignKey('ActivityType',verbose_name=' نوع النشاط الرئيسى / داعم ', on_delete=models.PROTECT,null=True,blank=True)
    #activity_type  domain='[("main_activity","=",main_activity),("entity_type","=",entity_type)]'

    affiliate = models.ForeignKey('Affiliate',verbose_name='الجهة التابعة', on_delete=models.PROTECT,null=True,blank=True)




    #reletd_filed  service_provider   relted with affiliate.service_provider  with string 'مقدم الخدمة'

    #reletd_filed  need_center   relted with affiliate.need_center  with string 'يجب إضافة منطقه او مركز ؟'

    #reletd_filed  main_activity_type   relted with main_activity.activity_type  with string 'رئيسى / داعم '
    center = models.ForeignKey('Center',verbose_name='المنطقة او المركز', on_delete=models.PROTECT,null=True,blank=True)
    branch = models.ForeignKey('Branch',verbose_name='الفرع', on_delete=models.PROTECT,null=True,blank=True)
    
    def __str__(self):
        return self.name
  
   
    # prevent XSS attackes 
    fields_to_escape = ['name','latitude','longitude']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
        

class MainSurveySection(models.Model):
    name = models.CharField(max_length=255,verbose_name='اسم قائمة الاستبيان الرئيسية')

    entity_type = models.CharField(max_length=500,verbose_name="نوع الاصل", choices=[('water','مياه شرب'),('sewage','صرف')],null=True,blank=True)

    main_activity = models.ForeignKey('MainActivity',verbose_name='النشاط الرئيسى / داعم', on_delete=models.PROTECT,null=True,blank=True)
    #main_activity  domain='[("entity_type","=",entity_type)]

    #reletd_filed  main_activity_type   relted with main_activity.activity_type  with string 'رئيسى / داعم '

    activity_type = models.ForeignKey('ActivityType',verbose_name=' نوع النشاط الرئيسى / داعم ', on_delete=models.PROTECT,null=True,blank=True)
    #activity_type  domain='[("main_activity","=",main_activity),("entity_type","=",entity_type)]'
    def __str__(self):
            return self.name
       
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        

class SubSurveySection(models.Model):
    name = models.CharField(max_length=255,verbose_name='اسم قائمة الاستبيان الفرعية')

    entity_type = models.CharField(max_length=500,verbose_name="نوع الاصل", choices=[('water','مياه شرب'),('sewage','صرف')],null=True,blank=True)

   
    main_survey_sections = models.ForeignKey('MainSurveySection',verbose_name=' قائمة الاستبيان الرئيسية', on_delete=models.PROTECT,null=True,blank=True)
    #  domain for main_survey_sections  domain="[('entity_type','=',entity_type)]"
    def __str__(self):
        return self.name
  
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        
        
class QuestionBank(models.Model):
    name = models.CharField(max_length=255,verbose_name='السؤال')

    sub_survey_sections = models.ManyToManyField('SubSurveySection',verbose_name=' قائمة الاستبيان الفرعية',)


    kpi_tags = models.ManyToManyField('SubSurveySection',related_name='questions_kpi_tags' , verbose_name=' مؤشرات الاداء' ,  blank=True)


    

    kpi = models.DecimalField(
        max_digits=30, 
  
        decimal_places=20, 
        
        
        verbose_name="المؤشر", 
        validators=[MinValueValidator(Decimal(0))], 
        null=True, blank=True
    )

    is_active = models.BooleanField(verbose_name ="نشط ؟")

    def __str__(self):
        return self.name
  
    # prevent XSS attackes 
    fields_to_escape = ['name']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        