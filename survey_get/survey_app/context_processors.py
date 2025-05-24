from django.urls import resolve
from django.apps import apps
from .utils import is_role_admin_fun


def dynamic_model_name(request):
    try:
        current_url_name = resolve(request.path_info).url_name 
        model_name = None

 
        model_mapping = {
            "activity_items_geo": "البيانات الجغرافية للمواقع",
            "governorates-list": "المحافظات",
            "governorates-form": "تعديل المحافظة",
            "governorates-create": "إضافة محافظة جديدة",
            "centers-list": "المراكز",
            "centers-form": "تعديل المركز",
            "centers-create": "إضافة مركز جديد",
            "service-providers-list": "مقدمو الخدمات",
            "service-providers-form": "تعديل مقدم الخدمة",
            "service-providers-create": "إضافة مقدم خدمة جديد",
            "affiliates-list": "الجهات التابعة",
            "affiliates-form": "تعديل الجهة التابعة",
            "affiliates-create": "إضافة جهة تابعة جديدة",
            "branches-list": "الفروع",
            "branches-form": "تعديل الفرع",
            "branches-create": "إضافة فرع جديد",
            "main-activity-list": "النشاط الرئيسي",
            "main-activity-form": "تعديل النشاط الرئيسي",
            "main-activity-create": "إضافة نشاط رئيسي جديد",
            "activity-types-list": "أنواع الأنشطة",
            "activity-types-form": "تعديل نوع النشاط",
            "activity-types-create": "إضافة نوع نشاط جديد",
            "activity-items-list": " الموقع ",
            "activity-items-form": "تعديل الموقع ",
            "activity-items-create": "إضافة  موقع جديد",
            "main-survey-sections-list": "القوائم الرئيسية للاستبيان",
            "main-survey-sections-form": "تعديل قائمة الاستبيان الرئيسي",
            "main-survey-sections-create": "إضافة قائمة استبيان رئيسي جديد",
            "sub-survey-sections-list": "القوائم  الفرعية للاستبيان",
            "sub-survey-sections-form": "تعديل قائمة الاستبيان الفرعي",
            "sub-survey-sections-create": "إضافة قائمة استبيان فرعي جديد",
            "question-bank-list": "بنك الأسئلة",
            "question-bank-form": "تعديل سؤال",
            "question-bank-create": "إضافة سؤال جديد",
            "survey-list": "الاستبيانات",
            "survey-form": "تعديل الاستبيان",
            "survey-create": "إضافة استبيان جديد",
            "400": "خطأ 400",
            "404": "خطأ 404",
            "500": "خطأ 500",
            "403": "خطأ 403",
            "home": "الرئيسية",
        }
        
             
 
        
        if current_url_name in model_mapping:
            model_name = model_mapping[current_url_name]

        return {"dynamic_model_name": model_name}
    
    except Exception:
        return {"dynamic_model_name": None}


def is_role_admin_fun_from_context(request):
    try:
        return {
            'is_role_admin_funfrom_context': is_role_admin_fun(request.user)
        }
    except Exception:
        return {
            'is_role_admin_funfrom_context': False
        }