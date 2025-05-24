from django import forms
from .all_models import main as base_models 
from .all_models import survey as survey_models  
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .custom_user import CustomUser
from django.utils import timezone
from django.forms import BaseModelFormSet
from django.utils import timezone
from django.db import transaction



class UserCreateForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة مرور جديدة',
        }),
        label="كلمة المرور الجديدة ",
    )
    
    class Meta:
        model = CustomUser
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'user_role': 'دور المستخدم',
            'login_state': 'حالة تسجيل الدخول',
            'user_custom_timezone': 'المنطقة الزمنية',
        }

        fields = [ 'first_name',"last_name", 'username','email',"user_role","new_password","login_state",'user_custom_timezone']  

        widgets = {
            
                        'first_name': forms.TextInput(attrs={
                'class': 'form-control',
           
            }),              'last_name': forms.TextInput(attrs={
                'class': 'form-control',
           
            }),
            
            'username': forms.TextInput(attrs={
                'class': 'form-control',
           
            }),
           'new_password': forms.TextInput(attrs={
                'class': 'form-control',
        
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
        
            }),
            'user_role': forms.Select(attrs={
                'class': 'form-control',
            }),
      
              'login_state': forms.Select(attrs={
                'class': 'form-control',    
      
            }),
              'user_custom_timezone': forms.Select(attrs={
                'class': 'form-control',    
      
            }),
          
            
           
        }
        
        
    def save(self, commit=True):

        user = super().save(commit=False)

        # Hash the new password if provided
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.password = make_password(new_password)

        if commit:
            user.save()
        return user
    

class UserUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة مرور جديدة',
        }),
        label="كلمة المرور الجديدة",
    )


    class Meta:
        model = CustomUser
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'user_role': 'دور المستخدم',
            'login_state': 'حالة تسجيل الدخول',
            'user_custom_timezone': 'المنطقة الزمنية',
        }
        fields = [ 'first_name',"last_name",'username','email',"user_role","new_password","login_state",'user_custom_timezone']  

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
           
            }),              'last_name': forms.TextInput(attrs={
                'class': 'form-control',
           
            }),       'username': forms.TextInput(attrs={
                'class': 'form-control',
           
            }),

      
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
        
            }), 
                 
            'new_password': forms.TextInput(attrs={
                'class': 'form-control',
        
            }),
            'user_role': forms.Select(attrs={
                'class': 'form-control',
            }),
              'login_state': forms.Select(attrs={
                'class': 'form-control',    
      
            }),
              'user_custom_timezone': forms.Select(attrs={
                'class': 'form-control',    
      
            }),
               
      
        }
        
        
        

    def save(self, commit=True):

        user = super().save(commit=False)

        # Hash the new password if provided
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.password = make_password(new_password)

        if commit:
            user.save()
        return user
    
 

















class SurveyCreateForm(forms.ModelForm):
    FIELD_MODEL_MAP = {
        'affiliate': base_models.Affiliate,
        'main_activity': base_models.MainActivity,
        'activity_type': base_models.ActivityType,
        'activity_item': base_models.ActivityItem,
        # 'main_survey_sections': base_models.MainSurveySection,
        'supporting_activity_item': base_models.ActivityItem,
        # 'supporting_main_survey_sections': base_models.MainSurveySection,
    }

    class Meta:
        model = survey_models.Survey
        fields = [
            'name',
            'date',
            'service_provider',
            'affiliate',
            'center',
            'origin_type',
            'main_activity',
            'activity_type',
            'activity_item',
            # 'main_survey_sections',
            'supporting_activity_item',
            # 'supporting_main_survey_sections',
            'visit_result',
            'visit_result_percntage',
            'questions_added',
            'visit_result_done',
            'full_mark',
            ]
        
        widgets = {
            
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
            
                'date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker',  # Custom class for JS picker
                'placeholder': 'Select a date and time', 
                'type': 'datetime-local',  
                          
                'data-cond': "name === 'hide'", 

            }),
     
            
            'service_provider': forms.Select(attrs={
                'class': 'form-control',}),
            
            'affiliate': forms.Select(attrs={
                'class': 'form-control',}),
            
            'center': forms.Select(attrs={
                'class': 'form-control',}),
            
            'origin_type': forms.Select(attrs={
                'class': 'form-control',}),
            
            'main_activity': forms.Select(attrs={
                'class': 'form-control',}),
            
            'activity_type': forms.Select(attrs={
                'class': 'form-control',}),
            
            
            'activity_item': forms.Select(attrs={
                'class': 'form-control',}),
            
            
            # 'main_survey_sections': forms.Select(attrs={
            #     'class': 'form-control',}),
            
            'supporting_activity_item': forms.Select(attrs={
                'class': 'form-control',}),
            
            # 'supporting_main_survey_sections': forms.Select(attrs={
            #     'class': 'form-control',}),
            
            
        }
      
      
      
    def __init__(self, *args, **kwargs):
        super(SurveyCreateForm, self).__init__(*args, **kwargs)
        
        for field, model in self.FIELD_MODEL_MAP.items():
                self.fields[field].queryset = model.objects.none()

        #  update queryset if form is submitted with data
        for field, model in self.FIELD_MODEL_MAP.items():
            field_value = self.data.get(field)
            if field_value:
                self.fields[field].queryset = model.objects.filter(pk=field_value)

        
        
         
   
    # def __init__(self, *args, **kwargs):
    #     super(SurveyCreateForm, self).__init__(*args, **kwargs)

    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         affiliate = self.instance.affiliate
    #         self.fields['affiliate'].queryset = base_models.Affiliate.objects.filter(pk=affiliate.pk)
       
    #         main_activity = self.instance.main_activity
    #         self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity.pk)
       
    #         activity_type = self.instance.activity_type
    #         self.fields['activity_type'].queryset = base_models.ActivityType.objects.filter(pk=activity_type.pk)
       
    #         activity_item = self.instance.activity_item
    #         self.fields['activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=activity_item.pk)
       
    #         main_survey_sections = self.instance.main_survey_sections
    #         self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=main_survey_sections.pk)
       
    #         supporting_activity_item = self.instance.supporting_activity_item
    #         self.fields['supporting_activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=supporting_activity_item.pk)
       
    #         supporting_main_survey_sections = self.instance.supporting_main_survey_sections
    #         self.fields['supporting_main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=supporting_main_survey_sections.pk)
       
       
    #     else:
    #         self.fields['affiliate'].queryset = base_models.Affiliate.objects.none()
    #         self.fields['main_activity'].queryset = base_models.MainActivity.objects.none()
    #         self.fields['activity_type'].queryset = base_models.ActivityType.objects.none()
    #         self.fields['activity_item'].queryset = base_models.ActivityItem.objects.none()
    #         self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.none()
    #         self.fields['supporting_activity_item'].queryset = base_models.ActivityItem.objects.none()
    #         self.fields['supporting_main_survey_sections'].queryset = base_models.MainSurveySection.objects.none()


    #     # If the form is submitted with data, update the queryset dynamically
    #     if 'affiliate' in self.data:
    #             affiliate = self.data.get('affiliate')
    #             self.fields['affiliate'].queryset = base_models.Affiliate.objects.filter(pk=affiliate)

    #     if 'main_activity' in self.data:
    #             main_activity = self.data.get('main_activity')
    #             self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity)

    #     if 'activity_type' in self.data:
    #             activity_type = self.data.get('activity_type')
    #             self.fields['activity_type'].queryset = base_models.ActivityType.objects.filter(pk=activity_type)

    #     if 'activity_item' in self.data:
    #             activity_item = self.data.get('activity_item')
    #             self.fields['activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=activity_item)

    #     if 'main_survey_sections' in self.data:
    #             main_survey_sections = self.data.get('main_survey_sections')
    #             self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=main_survey_sections)

    #     if 'supporting_activity_item' in self.data and  self.data["supporting_activity_item"] is not None and self.data["supporting_activity_item"] and self.data["supporting_activity_item"] !='' :
    #                 supporting_activity_item = self.data.get('supporting_activity_item')
    #                 self.fields['supporting_activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=supporting_activity_item)

    #     if 'supporting_main_survey_sections' in self.data:
    #                 supporting_main_survey_sections = self.data.get('supporting_main_survey_sections')
    #                 self.fields['supporting_main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=supporting_main_survey_sections)



class SurveyUpdateForm(forms.ModelForm):
    FIELD_MODEL_MAP = {
        'affiliate': base_models.Affiliate,
        'main_activity': base_models.MainActivity,
        'activity_type': base_models.ActivityType,
        'activity_item': base_models.ActivityItem,
        # 'main_survey_sections': base_models.MainSurveySection,
        'supporting_activity_item': base_models.ActivityItem,
        # 'supporting_main_survey_sections': base_models.MainSurveySection,
    }
    last_refresh_time = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = survey_models.Survey
        fields = [
            'name',
    
            'date',
            'service_provider',
            'affiliate',
            'center',
            'origin_type',
            'main_activity',
            'activity_type',
            'activity_item',
            # 'main_survey_sections',
            'supporting_activity_item',
            # 'supporting_main_survey_sections',
            'visit_result',
            'full_mark',
            'visit_result_percntage',
            'questions_added',
            'visit_result_done',
            'last_refresh_time',  
            ]
            
        widgets = {
                      'last_refresh_time': forms.HiddenInput(),
                'name': forms.TextInput(attrs={
                    'class': 'form-control',}),
                
                'date': forms.DateTimeInput(attrs={
                    'class': 'form-control datetimepicker',  # Custom class for JS picker
                    'placeholder': 'Select a date and time', 
                    'type': 'datetime-local',  
        

                }),
                    
                'service_provider': forms.Select(attrs={
                    'class': 'form-control',}),
                
                'affiliate': forms.Select(attrs={
                    'class': 'form-control',}),
                
                'center': forms.Select(attrs={
                    'class': 'form-control',}),
                
                'origin_type': forms.Select(attrs={
                    'class': 'form-control',}),
                
                'main_activity': forms.Select(attrs={
                    'class': 'form-control',}),
                
                'activity_type': forms.Select(attrs={
                    'class': 'form-control',}),
                
                
                'activity_item': forms.Select(attrs={
                    'class': 'form-control',}),
                
                
                # 'main_survey_sections': forms.Select(attrs={
                    # 'class': 'form-control',}),
                
                'supporting_activity_item': forms.Select(attrs={
                    'class': 'form-control',}),
                
                # 'supporting_main_survey_sections': forms.Select(attrs={
                    # 'class': 'form-control',}),
                    
                
            }
            



    def __init__(self, *args, **kwargs):
        super(SurveyUpdateForm, self).__init__(*args, **kwargs)

        # Make all fields readonly if survey is confirmed
        if self.instance and self.instance.state not in  ["draft"] :
            for field_name, field in self.fields.items():
                field.disabled = True
                
                
        if self.instance and self.instance.pk:  # Editing an existing record
            # self.fields["last_refresh_time"].initial = timezone.now()  # Store  refresh time
            self.fields["last_refresh_time"].initial = timezone.now().isoformat()  # Store  refresh time
            
            for field, model in self.FIELD_MODEL_MAP.items():
                instance_value = getattr(self.instance, field, None)
                if instance_value and instance_value !='' and instance_value !='NoneType'  and instance_value  is not None:
      
                    self.fields[field].queryset = model.objects.filter(pk=instance_value.pk)
            
            else :
                    self.fields[field].queryset = model.objects.none()
                
        else:
            for field, model in self.FIELD_MODEL_MAP.items():
                self.fields[field].queryset = model.objects.none()

        # Dynamically update queryset if form is submitted with data
        for field, model in self.FIELD_MODEL_MAP.items():
            field_value = self.data.get(field)
            if field_value:
                self.fields[field].queryset = model.objects.filter(pk=field_value)

        

    # def clean(self):
    #     """ Compare last_refresh_time with last_updated before saving """
    #     cleaned_data = super().clean()

    #     if self.instance.pk:  # Only check for existing records
    #         record = survey_models.Survey.objects.get(pk=self.instance.pk)
    #         record_current_last_updated = record.last_updated

    #         # Get last refresh time from the hidden field
    #         last_refresh_time = cleaned_data.get("last_refresh_time")

    #         print("##############")  
    #         print(cleaned_data, "cleaned_data")  
    #         print(self.instance.pk, "self.instance:")  
    #         print(last_refresh_time, "last_refresh_time:")  
    #         print(record_current_last_updated, "record_current_last_updated")  
    #         print("##############")  

    #         if last_refresh_time and record_current_last_updated > last_refresh_time:
    #             raise ValidationError("This survey was updated by another user. Please refresh and try again.")

    #     return cleaned_data




    # def __init__(self, *args, **kwargs):
    #     super(SurveyUpdateForm, self).__init__(*args, **kwargs)

    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         affiliate = self.instance.affiliate
    #         self.fields['affiliate'].queryset = base_models.Affiliate.objects.filter(pk=affiliate.pk)
       
    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         main_activity = self.instance.main_activity
    #         self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity.pk)
       
    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         activity_type = self.instance.activity_type
    #         self.fields['activity_type'].queryset = base_models.ActivityType.objects.filter(pk=activity_type.pk)
       
    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         activity_item = self.instance.activity_item
    #         self.fields['activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=activity_item.pk)
       
    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         main_survey_sections = self.instance.main_survey_sections
    #         self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=main_survey_sections.pk)
       
    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         supporting_activity_item = self.instance.supporting_activity_item
    #         self.fields['supporting_activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=supporting_activity_item.pk)
       
    #     if self.instance and self.instance.pk:  # Editing an existing record
    #         supporting_main_survey_sections = self.instance.supporting_main_survey_sections
    #         self.fields['supporting_main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=supporting_main_survey_sections.pk)
       
    #     else:
    #         self.fields['affiliate'].queryset = base_models.Affiliate.objects.none()
    #         self.fields['main_activity'].queryset = base_models.MainActivity.objects.none()
    #         self.fields['activity_type'].queryset = base_models.ActivityType.objects.none()
    #         self.fields['activity_item'].queryset = base_models.ActivityItem.objects.none()
    #         self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.none()
    #         self.fields['supporting_activity_item'].queryset = base_models.ActivityItem.objects.none()
    #         self.fields['supporting_main_survey_sections'].queryset = base_models.MainSurveySection.objects.none()


    #     # If the form is submitted with data, update the queryset dynamically
    #     if 'affiliate' in self.data:
    #             affiliate = self.data.get('affiliate')
    #             self.fields['affiliate'].queryset = base_models.Affiliate.objects.filter(pk=affiliate)

    #     if 'main_activity' in self.data:
    #             main_activity = self.data.get('main_activity')
    #             self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity)

    #     if 'activity_type' in self.data:
    #             activity_type = self.data.get('activity_type')
    #             self.fields['activity_type'].queryset = base_models.ActivityType.objects.filter(pk=activity_type)

    #     if 'activity_item' in self.data:
    #             activity_item = self.data.get('activity_item')
    #             self.fields['activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=activity_item)

    #     if 'main_survey_sections' in self.data:
    #             main_survey_sections = self.data.get('main_survey_sections')
    #             self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=main_survey_sections)

    #     if 'supporting_activity_item' in self.data:
    #                 supporting_activity_item = self.data.get('supporting_activity_item')
    #                 self.fields['supporting_activity_item'].queryset = base_models.ActivityItem.objects.filter(pk=supporting_activity_item)

    #     if 'supporting_main_survey_sections' in self.data:
    #                 supporting_main_survey_sections = self.data.get('supporting_main_survey_sections')
    #                 self.fields['supporting_main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=supporting_main_survey_sections)


      







class GovernoratesCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.Governorate
        fields = ['name',"latitude","longitude"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),

      'latitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),

      'longitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),

        }
        
       


class GovernoratesUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.Governorate
        fields = ['name',"latitude","longitude"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),

                      'latitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),

      'longitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),
        }
        

class CentersUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.Center
        fields = ['name','governorate']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
            'governorate': forms.Select(attrs={
                'class': 'form-control',})


        }
        
       


class CentersCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.Center
        fields = ['name','governorate']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
            'governorate': forms.Select(attrs={
                'class': 'form-control',})


        }

class ServiceProviderCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.ServiceProvider
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',})
        }
        
       


class ServiceProviderUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.ServiceProvider
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',})
        }
        

class AffiliateCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.Affiliate
        fields = ['name','entity_type','service_provider','need_center']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),

                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),

                
            'service_provider': forms.Select(attrs={
                'class': 'form-control',}),

                
            'need_center': forms.CheckboxInput(attrs={
                'class': 'form_bool',}),


        }
        
       


class AffiliateUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.Affiliate
        fields = ['name','entity_type','service_provider','need_center']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),

                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),

                
            'service_provider': forms.Select(attrs={
                'class': 'form-control',}),

                
            'need_center': forms.CheckboxInput(attrs={
                'class': 'form_bool',}),


        }
        

class BranchesUpdateForm(forms.ModelForm):

    class Meta:
        model = base_models.Branch
        fields = ['name','affiliate']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'affiliate': forms.Select(attrs={
                'class': 'form-control',}),
        
        }
        
  

class BranchesCreateForm(forms.ModelForm):

    class Meta:
        model = base_models.Branch
        fields = ['name','affiliate']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
     
            'affiliate': forms.Select(attrs={
                'class': 'form-control',}),

        }
        

class MainActivityUpdateForm(forms.ModelForm):

    class Meta:
        model = base_models.MainActivity
        fields = ['name','entity_type','activity_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'activity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
        }
        
  

class MainActivityCreateForm(forms.ModelForm):

   
    class Meta:
        model = base_models.MainActivity
        fields = ['name','entity_type','activity_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'activity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
        }



     

class ActivityTypeUpdateForm(forms.ModelForm):

    class Meta:
        model = base_models.ActivityType
        fields = ['name','entity_type','main_activity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'main_activity': forms.Select(attrs={
                'class': 'form-control',}),
        
        }
    def __init__(self, *args, **kwargs):
        super(ActivityTypeUpdateForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:  # Editing an existing record
   
            main_activity = self.instance.main_activity
            self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity.pk)
        else:
            self.fields['main_activity'].queryset = base_models.MainActivity.objects.none()

        # If the form is submitted with data, update the queryset dynamically
        if 'main_activity' in self.data:
                main_activity = self.data.get('main_activity')
                self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity)


            
            
class ActivityTypeCreateForm(forms.ModelForm):

    class Meta:
        model = base_models.ActivityType
        fields = ['name','entity_type','main_activity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'main_activity': forms.Select(attrs={
                'class': 'form-control',}),
        
        }

    def __init__(self, *args, **kwargs):
        super(ActivityTypeCreateForm, self).__init__(*args, **kwargs)
    

        if not self.data: 
            self.fields['main_activity'].queryset = base_models.MainActivity.objects.none()
        else:  # Form submitted
            main_activity = self.data.get('main_activity')
            if main_activity:
                self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity)

            

            
class ActivityItemsUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.ActivityItem
        fields = ['name',"latitude","longitude",'entity_type','main_activity','activity_type','affiliate','center','branch']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                'latitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),

      'longitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'main_activity': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'activity_type': forms.Select(attrs={
                'class': 'form-control',}),

        
                
            'affiliate': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'center': forms.Select(attrs={
                'class': 'form-control',}),

        
                
            'branch': forms.Select(attrs={
                'class': 'form-control',}),

        }

            
class ActivityItemsCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.ActivityItem
        fields = ['name','latitude','longitude','entity_type','main_activity','activity_type','affiliate','center','branch']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                                      'latitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),

      'longitude': forms.TextInput(attrs={
                'class': 'form-control',
        
                }),
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'main_activity': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'activity_type': forms.Select(attrs={
                'class': 'form-control',}),

        
                
            'affiliate': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'center': forms.Select(attrs={
                'class': 'form-control',}),

        
                
            'branch': forms.Select(attrs={
                'class': 'form-control',}),

        }




    def __init__(self, *args, **kwargs):
        super(ActivityItemsCreateForm, self).__init__(*args, **kwargs)
    

        if not self.data: 
            self.fields['main_activity'].queryset = base_models.MainActivity.objects.none()
            self.fields['activity_type'].queryset = base_models.ActivityType.objects.none()
        else:  # Form submitted
            main_activity = self.data.get('main_activity')
            activity_type = self.data.get('activity_type')
            if main_activity:
                self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity)
            if activity_type :
                self.fields['activity_type'].queryset = base_models.ActivityType.objects.filter(pk=activity_type)






         
class MainSurveySectionCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.MainSurveySection
        fields = ['name','entity_type','main_activity','activity_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'main_activity': forms.Select(attrs={
                'class': 'form-control',}),
   
                
            'activity_type': forms.Select(attrs={
                'class': 'form-control',}),
   

        }



    def __init__(self, *args, **kwargs):
        super(MainSurveySectionCreateForm, self).__init__(*args, **kwargs)
    

        if not self.data: 
            self.fields['main_activity'].queryset = base_models.MainActivity.objects.none()
            self.fields['activity_type'].queryset = base_models.ActivityType.objects.none()
        else:  # Form submitted
            main_activity = self.data.get('main_activity')
            activity_type = self.data.get('activity_type')
            if main_activity:
                self.fields['main_activity'].queryset = base_models.MainActivity.objects.filter(pk=main_activity)
            if activity_type :
                self.fields['activity_type'].queryset = base_models.ActivityType.objects.filter(pk=activity_type)








         
class MainSurveySectionUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.MainSurveySection
        fields = ['name','entity_type','main_activity','activity_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
                
            'main_activity': forms.Select(attrs={
                'class': 'form-control',}),
   
                
            'activity_type': forms.Select(attrs={
                'class': 'form-control',}),
   

        }




         
class SubSurveySectionUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.SubSurveySection
        fields = ['name','entity_type','main_survey_sections']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
       
                
            'main_survey_sections': forms.Select(attrs={
                'class': 'form-control',}),
   

        }

         
class SubSurveySectionCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.SubSurveySection
        fields = ['name','entity_type','main_survey_sections']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),
                
            'entity_type': forms.Select(attrs={
                'class': 'form-control',}),
        
       
                
            'main_survey_sections': forms.Select(attrs={
                'class': 'form-control',}),
   

        }


    def __init__(self, *args, **kwargs):
        super(SubSurveySectionCreateForm, self).__init__(*args, **kwargs)
    

        if not self.data: 
            self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.none()
            
        else:  # Form submitted
            main_survey_sections = self.data.get('main_survey_sections')
      
            if main_survey_sections:
                self.fields['main_survey_sections'].queryset = base_models.MainSurveySection.objects.filter(pk=main_survey_sections)



class QuestionBankCreateForm(forms.ModelForm):
    class Meta:
        model = base_models.QuestionBank
        fields = ['name','sub_survey_sections',"kpi_tags",'kpi','is_active']
        widgets = {
            
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),

            'sub_survey_sections': forms.SelectMultiple(attrs={
                'class': 'form-control',}),
            
            'kpi_tags': forms.SelectMultiple(attrs={
                'class': 'form-control',}),
            
            
            
      'kpi': forms.NumberInput(attrs={
                'class': 'form-control',
                # 'step': '0.00000000000000000001',  
 
               
                }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form_bool',}),
        }
        
       


class QuestionBankUpdateForm(forms.ModelForm):
    class Meta:
        model = base_models.QuestionBank
        fields = ['name','sub_survey_sections',"kpi_tags",'kpi','is_active']
        widgets = {
            
            'name': forms.TextInput(attrs={
                'class': 'form-control',}),

            'sub_survey_sections': forms.SelectMultiple(attrs={
                'class': 'form-control',}),

            'kpi_tags': forms.SelectMultiple(attrs={
                'class': 'form-control',}),

                 'kpi': forms.NumberInput(attrs={
                'class': 'form-control',
                #  'step': '0.00000000000000000001',  
       
                }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form_bool',}),
        }
        