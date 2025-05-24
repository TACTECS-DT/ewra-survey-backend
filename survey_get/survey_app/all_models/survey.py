from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.validators import MinValueValidator ,MaxValueValidator
from django.db.models import ProtectedError
from decimal import Decimal
from django.utils.html import escape
from .attachment import Attachment  
from django.contrib.contenttypes.fields import GenericRelation

class Survey(models.Model):
    
    STATE_CHOICES = [
        ('draft', 'مسودة'),
        ('in_progress', 'جارى العمل عليه'),
        ('confirmed', 'تم التأكيد'),
        ('cancelled', 'تم الالغاء'),
    ]
    
    last_updated = models.DateTimeField(auto_now=True)  # Auto-update on changes
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='draft')
    
    
    name = models.TextField( verbose_name="اسم الاستبيان")

    date = models.DateTimeField(verbose_name="تاريخ الزيارة")

    service_provider = models.ForeignKey('ServiceProvider', on_delete=models.PROTECT, verbose_name="مقدم الخدمة")


    affiliate = models.ForeignKey('Affiliate', on_delete=models.PROTECT, verbose_name="الجهة التابعة",null=True,blank=True)
    #affiliate domain="[('service_provider','=',service_provider)]"
   


    # related need_center  affiliate.need_center  string='يجب إضافة منطقه او مركز ؟ '


    center = models.ForeignKey('Center', on_delete=models.PROTECT, verbose_name="المنطقة او المركز",null=True,blank=True)



    # related entity_type affiliate.entity_type , string='نوع الخدمة الخاصة بالجهة التابعة'


    origin_type = models.CharField(
        max_length=50,
        choices=[('water', 'مياه شرب'), ('sewage', 'صرف')],
        verbose_name="نوع الأصل"
    ,null=True,blank=True)


    


    main_activity = models.ForeignKey(
        'MainActivity', 
        on_delete=models.PROTECT, 
        verbose_name="النشاط الرئيسى / داعم"
        
    ,null=True,blank=True)
    #main_activity domain='[("entity_type","=",origin_type)]'

    

    activity_type = models.ForeignKey('ActivityType',verbose_name=' نوع النشاط الرئيسى / داعم ', on_delete=models.PROTECT,null=True,blank=True)
    #activity_type  domain='[("main_activity","=",main_activity),("entity_type","=",origin_type)]'
 
 


    activity_item = models.ForeignKey('ActivityItem',verbose_name='النشاط', on_delete=models.PROTECT , related_name="activity_item_surveys",null=True,blank=True)
    #activity_item domain='[("entity_type","=",origin_type),("activity_type","=",activity_type),("affiliate_id","=",affiliate_id)]',

 

    # main_survey_sections = models.ForeignKey('MainSurveySection',verbose_name=' قائمة الاستبيان الرئيسية', on_delete=models.PROTECT,        related_name="main_survey_sections_surveys" ,null=True,blank=True)
    #main_survey_sections domain="[('activity_type','=',activity_type),('entity_type','=',origin_type)]",

 

    #related main_activity_type with   main_activity.activity_type string='رئيسى / داعم '



    supporting_activity_item = models.ForeignKey('ActivityItem',verbose_name='النشاط', on_delete=models.PROTECT, related_name="supporting_activity_item_surveys"  ,null=True,blank=True)
    #supporting_activity_item  domain='[("entity_type","=",origin_type),("main_activity","=",main_activity),("affiliate_id","=",affiliate_id)]'


 

    # supporting_main_survey_sections = models.ForeignKey('MainSurveySection',verbose_name=' قائمة الاستبيان الرئيسية', on_delete=models.PROTECT,        related_name="supporting_main_survey_sections_surveys" ,null=True,blank=True)
    #supporting_main_survey_sections  domain="[('main_activity','=',main_activity),('entity_type','=',origin_type)]"


    full_mark = models.DecimalField(
        max_digits=30, 

        decimal_places=20, 
        
        
        null=True,
        blank=True,
        verbose_name="الدرجة النهائية", 
        validators=[MinValueValidator(Decimal(0))]
    )

    visit_result = models.DecimalField(
         max_digits=30, 

        decimal_places=20, 
        
        
        
        null=True,
        blank=True,
        verbose_name="نتيجة الاستبيان", 
        validators=[MinValueValidator(Decimal(0))]
    )


    visit_result_percntage = models.DecimalField(
             max_digits=30, 

        decimal_places=20, 
        
        
               validators=[MinValueValidator(Decimal(0))], 
        
             null=True,
        blank=True ,
        verbose_name="نتيجة الاستبيان المؤية", 
      
    )
    # readonly=True
    

    questions_added = models.BooleanField(default=False, verbose_name="تم اضافة الاسئلة",null=True,
        blank=True )
    # readonly=True

    visit_result_done = models.BooleanField(default=False, verbose_name="تم حساب النتيجة",null=True,
        blank=True )
    # readonly=True


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
        



class SurveyQuestion(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    question = models.ForeignKey('QuestionBank', on_delete=models.PROTECT, verbose_name="السؤال")
    last_updated = models.DateTimeField(auto_now=True)  
    
    attachments = GenericRelation(Attachment, related_query_name='survey_question_attachments')


    kpi = models.DecimalField(
        max_digits=30, 
   
        decimal_places=20, 
               validators=[MinValueValidator(Decimal(0))], 
        verbose_name="المؤشر", 
        null=True, blank=True
    )

    answer_percentage = models.DecimalField(
             max_digits=30, 
 
        decimal_places=20, 
               validators=[MinValueValidator(Decimal(0))], 
        verbose_name="الدرجة",
             
          null=True,blank=True
    )  # Store as a fraction (0-1)

    answer_notes = models.TextField(verbose_name="ملحوظات", blank=True, null=True)
    answer_recommendations = models.TextField(verbose_name="توصيات", blank=True, null=True)


    sub_survey_section = models.ForeignKey('SubSurveySection', on_delete=models.PROTECT, verbose_name="قائمة الاستبيان الفرعية")
    
    main_survey_section = models.ForeignKey('MainSurveySection', on_delete=models.PROTECT, verbose_name="قائمة الاستبيان الرئيسية ")
    

    kpi_sub_total = models.DecimalField(
        max_digits=30, 

        decimal_places=20, 
        
        
        verbose_name="المجموع الجزئى", 
 
        validators=[MinValueValidator(Decimal(0))], 
        null=True, blank=True
    )

    last_updated = models.DateTimeField(auto_now=True,verbose_name="تاريخ التعديل")
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="تم التعديل بواسطة"
    )


    # def get_last_updated_user(self):
    #     last_update = self.update_histories.order_by('-updated_at').first()
    #     return last_update.updated_by if last_update else None  # Return user or None
    
    def __str__(self):
        return f"{self.survey} - {self.question}"
    


    # prevent XSS attackes 
    fields_to_escape = ['name',"answer_notes",'answer_recommendations']
    
    def save(self, *args, **kwargs):
        for field in self.fields_to_escape:
            value = getattr(self, field, None)
            if isinstance(value, str):
                setattr(self, field, escape(value))
        super().save(*args, **kwargs)
        


# class SurveyQuestionsUpdateHistory(models.Model):
    
#     survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name="update_histories")
#     updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="تم التعديل بواسطة",related_name="updated_surveys")
#     updated_at = models.DateTimeField(verbose_name="تاريخ التعديل")

#     class Meta:
#         verbose_name = "تاريخ التعديل"
#         verbose_name_plural = "تواريخ التعديل"
        
        

