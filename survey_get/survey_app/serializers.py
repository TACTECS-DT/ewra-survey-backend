from rest_framework import serializers
from .utils import get_choice_field_value   
from . import models as all_models
from decimal import Decimal




# //////////Governorate//////////////

class Governorate_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()

class Governorate_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        latitude = serializers.CharField()
        longitude = serializers.CharField()
        
class Governorate_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        latitude = serializers.CharField()
        longitude = serializers.CharField()
        
        def update(self, instance, validated_data):
            updated = False  


            fields_to_update =   ['name', 'latitude','longitude']               


            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
        def create(self, validated_data):
            return all_models.Governorate.objects.create(**validated_data)



        
# ////////////Center////////////


class Center_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()

class Center_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        governorate = Governorate_Related_GET_Serializer()




class Center_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        governorate = serializers.PrimaryKeyRelatedField(queryset=all_models.Governorate.objects.all())



        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

       
        def update(self, instance, validated_data):
            updated = False  


            fields_to_update =   [
                        'name',
                        'governorate',
                      ]               


            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    


        def create(self, validated_data):
            return all_models.Center.objects.create(**validated_data)


# ////////////////////////
      
# ////////////ServiceProvider////////////


class ServiceProvider_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()

class ServiceProvider_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
   

class ServiceProvider_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
   
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

       
        def update(self, instance, validated_data):
            updated = False  


            fields_to_update =   [
                        'name',   
                      ]               

            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True
            if updated:
                instance.save()

            return instance


        def create(self, validated_data):
            return all_models.ServiceProvider.objects.create(**validated_data)



# ////////////////////////
      
# ////////////Affiliate////////////


class Affiliate_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()

class Affiliate_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        entity_type = serializers.SerializerMethodField(method_name="get_entity_type")
        service_provider = ServiceProvider_Related_GET_Serializer()
        need_center = serializers.BooleanField()
   
        def get_entity_type(self, obj):
                return get_choice_field_value(obj, 'entity_type') 


class Affiliate_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        entity_type = serializers.ChoiceField(choices=[('water', 'مياه شرب'), ('sewage', 'صرف')])
        service_provider = serializers.PrimaryKeyRelatedField(queryset=all_models.ServiceProvider.objects.all())
        need_center = serializers.BooleanField()
        
        
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

        def update(self, instance, validated_data):
            updated = False  
            fields_to_update =   [
                        'name',
                        'entity_type',
                        'service_provider',
                        'need_center',
                         ]               

            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
        def create(self, validated_data):
            return all_models.Affiliate.objects.create(**validated_data)



# ////////////////////////
 
# ////////////Branch////////////


class Branch_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()

class Branch_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        affiliate = Affiliate_Related_GET_Serializer()


class Branch_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        affiliate = serializers.PrimaryKeyRelatedField(queryset=all_models.Affiliate.objects.all())


    
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

        def update(self, instance, validated_data):
            updated = False  
            fields_to_update =   [
                        'name',
                        'affiliate',
                         ]               

            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
        def create(self, validated_data):
            return all_models.Branch.objects.create(**validated_data)


# ////////////////////////

# //////////MainActivity//////////////

class MainActivity_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()


class MainActivity_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        entity_type = serializers.SerializerMethodField(method_name="get_entity_type")
        activity_type = serializers.SerializerMethodField(method_name="get_activity_type")
        
        def get_entity_type(self, obj):
                return get_choice_field_value(obj, 'entity_type') 

        def get_activity_type(self, obj):
                return get_choice_field_value(obj, 'activity_type') 



class MainActivity_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        entity_type = serializers.ChoiceField(choices=[('water', 'مياه شرب'), ('sewage', 'صرف')])
        activity_type = serializers.ChoiceField(choices=[('main','رئيسى'),('supporter','داعم'),])

    
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

        def update(self, instance, validated_data):
            updated = False  
            fields_to_update =   [
                        'name',
                        'entity_type',
                        'activity_type',
                       ]               

            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
        def create(self, validated_data):
            return all_models.MainActivity.objects.create(**validated_data)




# ////////////////////////

# //////////ActivityType//////////////

class ActivityType_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()


class ActivityType_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        entity_type = serializers.SerializerMethodField(method_name='get_entity_type')
        main_activity = MainActivity_Related_GET_Serializer()
    
        
        def get_entity_type(self, obj):
                return get_choice_field_value(obj, 'entity_type') 


class ActivityType_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        entity_type = serializers.ChoiceField(choices=[('water', 'مياه شرب'), ('sewage', 'صرف')])
        main_activity = serializers.PrimaryKeyRelatedField(queryset=all_models.MainActivity.objects.all())
    
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

        def update(self, instance, validated_data):
            updated = False  
            fields_to_update =   [
                        'name',
                        'entity_type',
                        'main_activity', ]               

            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
        def create(self, validated_data):
            return all_models.ActivityType.objects.create(**validated_data)



# ////////////////////////

# //////////ActivityItem//////////////

class ActivityItem_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()


class ActivityItem_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        entity_type = serializers.SerializerMethodField(method_name='get_entity_type')        
        latitude = serializers.CharField()
        longitude = serializers.CharField()
        main_activity = MainActivity_Related_GET_Serializer()
        activity_type = ActivityType_Related_GET_Serializer()
        affiliate = Affiliate_Related_GET_Serializer()
        center = Center_Related_GET_Serializer()
        branch = Branch_Related_GET_Serializer()
              
#        get selection value and key 
        def get_entity_type(self, obj):
                return get_choice_field_value(obj, 'entity_type') 
        
class ActivityItem_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        latitude = serializers.CharField(required=False)
        longitude = serializers.CharField(required=False)
        entity_type = serializers.ChoiceField(choices=[('water', 'مياه شرب'), ('sewage', 'صرف')])
        main_activity = serializers.PrimaryKeyRelatedField(queryset=all_models.MainActivity.objects.all())
        activity_type = serializers.PrimaryKeyRelatedField(queryset=all_models.ActivityType.objects.all())
        affiliate = serializers.PrimaryKeyRelatedField(queryset=all_models.Affiliate.objects.all())
        center = serializers.PrimaryKeyRelatedField(queryset=all_models.Center.objects.all())
        branch = serializers.PrimaryKeyRelatedField(queryset=all_models.Branch.objects.all())
        
    
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

       
        def update(self, instance, validated_data):
            updated = False  


            fields_to_update =   [
                        'name',
                        'entity_type',
                        'latitude',
                        'longitude',
                        'main_activity',
                        'activity_type',
                        'affiliate',
                        'center',
                        'branch'
                         ]               


            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    


# to map create with  creation model 
        def create(self, validated_data):
            return all_models.ActivityItem.objects.create(**validated_data)



# ////////////////////////

# //////////MainSurveySection//////////////

class MainSurveySection_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()


class MainSurveySection_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        entity_type = serializers.SerializerMethodField(method_name='get_entity_type')        
        main_activity = MainActivity_Related_GET_Serializer()
        activity_type = ActivityType_Related_GET_Serializer()

        def get_entity_type(self, obj):
                return get_choice_field_value(obj, 'entity_type') 
        
        

class MainSurveySection_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        entity_type = serializers.ChoiceField(choices=[('water', 'مياه شرب'), ('sewage', 'صرف')])
        
        main_activity = serializers.PrimaryKeyRelatedField(queryset=all_models.MainActivity.objects.all())
        activity_type = serializers.PrimaryKeyRelatedField(queryset=all_models.ActivityType.objects.all())
       
        
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

        def update(self, instance, validated_data):
            updated = False  
            fields_to_update =   [
                        'name',
                        'entity_type',
                        'main_activity',
                        'activity_type', ]               

            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
        def create(self, validated_data):
            return all_models.MainSurveySection.objects.create(**validated_data)
        
# ////////////////////////




# //////////SubSurveySection//////////////

class SubSurveySection_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()


class SubSurveySection_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        entity_type = serializers.SerializerMethodField(method_name='get_entity_type')
        main_survey_sections = MainSurveySection_Related_GET_Serializer()

        def get_entity_type(self, obj):
                return get_choice_field_value(obj, 'entity_type') 
        
        

class SubSurveySection_PATCH_POST_Serializer(serializers.Serializer):
        name = serializers.CharField()
        entity_type = serializers.ChoiceField(choices=[('water', 'مياه شرب'), ('sewage', 'صرف')])
        main_survey_sections = serializers.PrimaryKeyRelatedField(queryset=all_models.MainSurveySection.objects.all())

  
        
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

        def update(self, instance, validated_data):
            updated = False  
            fields_to_update =   [
                        'name',
                        'entity_type',
                        'main_survey_sections']               

            for field in fields_to_update:
                new_value = validated_data.get(field)       
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
        def create(self, validated_data):
            return all_models.SubSurveySection.objects.create(**validated_data)



        
        
# ////////////////////////


# //////////KPITag//////////////

class  KPITags_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()

# //////////QuestionBank//////////////

class QuestionBank_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()


class QuestionBank_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        
        # many2many
        sub_survey_sections = SubSurveySection_Related_GET_Serializer(many=True)  
        kpi_tags = KPITags_Related_GET_Serializer(many=True)  

        kpi = serializers.DecimalField( max_digits=30, decimal_places=20, max_value=Decimal('1.00000000000000000000'),min_value=Decimal(0))
        is_active = serializers.BooleanField()



class QuestionBank_PATCH_POST_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        
        # many2many
        sub_survey_sections =   serializers.PrimaryKeyRelatedField(
        queryset=all_models.SubSurveySection.objects.all(),
        many=True ) 
        
        # many2many
        kpi_tags = serializers.PrimaryKeyRelatedField(
        queryset=all_models.SubSurveySection.objects.all(),
        many=True ) 

#         
        kpi = serializers.DecimalField( max_digits=30, decimal_places=20, max_value=Decimal('1.00000000000000000000'),min_value=Decimal(0))
        is_active = serializers.BooleanField()




        def update(self, instance, validated_data):
            updated = False
            m2m_fields = ['sub_survey_sections', 'kpi_tags']
            normal_fields = ['name', 'kpi', 'is_active']

            # Update normal fields
            for field in normal_fields:
                new_value = validated_data.get(field)
                if new_value is not None and getattr(instance, field) != new_value:
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()

            # Update M2M fields separately
            for field in m2m_fields:
                if field in validated_data:
                    new_value = validated_data.get(field)
                    getattr(instance, field).set(new_value)
            return instance





        def create(self, validated_data):
            m2m_fields = {
                'sub_survey_sections': validated_data.pop('sub_survey_sections', []),
                'kpi_tags': validated_data.pop('kpi_tags', []),
            }

            instance = all_models.QuestionBank.objects.create(**validated_data)

            for field, value in m2m_fields.items():
                getattr(instance, field).set(value)

            return instance
        
        

        
# //////////Survey//////////////


class Survey_Related_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()


class Survey_FORM_GET_Serializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        
        name = serializers.CharField()
        
        date = serializers.DateTimeField()
        last_updated = serializers.DateTimeField()
        
        service_provider = ServiceProvider_Related_GET_Serializer()
        
        affiliate = Affiliate_Related_GET_Serializer()
        
        center = Center_Related_GET_Serializer()
        
        origin_type = serializers.SerializerMethodField(method_name='get_origin_type')
        
        state = serializers.SerializerMethodField(method_name='get_state')
        
        main_activity = MainActivity_Related_GET_Serializer()
        
        activity_type = ActivityType_Related_GET_Serializer()
        
        activity_item = ActivityItem_Related_GET_Serializer()
        
        supporting_activity_item = ActivityItem_Related_GET_Serializer()
        
        full_mark = serializers.DecimalField(max_digits=30,decimal_places=20,min_value=Decimal(0))
        
        visit_result = serializers.DecimalField(max_digits=30,decimal_places=20,min_value=Decimal(0))

        visit_result_percntage = serializers.DecimalField(max_digits=30,decimal_places=20,min_value=Decimal(0))
        
        questions_added = serializers.BooleanField()
        
        visit_result_done = serializers.BooleanField()




        def get_origin_type(self, obj):
                return get_choice_field_value(obj, 'origin_type') 
        

        def get_state(self, obj):
                return get_choice_field_value(obj, 'state') 
        



class Survey_PATCH_POST_Serializer(serializers.Serializer):
        
        name = serializers.CharField()
        
        date = serializers.DateTimeField()
        
        service_provider = serializers.PrimaryKeyRelatedField(
        queryset=all_models.ServiceProvider.objects.all())
        
        affiliate = serializers.PrimaryKeyRelatedField(
        queryset=all_models.Affiliate.objects.all())
        
        center = serializers.PrimaryKeyRelatedField(
        queryset=all_models.Center.objects.all())
        
        origin_type = serializers.ChoiceField(choices=[('water', 'مياه شرب'), ('sewage', 'صرف')])
                    
        main_activity = serializers.PrimaryKeyRelatedField(queryset=all_models.MainActivity.objects.all())
        
        activity_type = serializers.PrimaryKeyRelatedField(queryset=all_models.ActivityType.objects.all())
        
        activity_item = serializers.PrimaryKeyRelatedField(queryset=all_models.ActivityItem.objects.all())
        
        supporting_activity_item = serializers.PrimaryKeyRelatedField(queryset=all_models.ActivityItem.objects.all())
        
        

        
        

        
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Name cannot be empty.")
            return value

        def update(self, instance, validated_data):
            updated = False  
            fields_to_update =   [
                            "name",
                            "date",
                            "service_provider",
                            "affiliate",
                            "center",
                            "origin_type",
                            "main_activity",
                            "activity_type",
                            "activity_item",
                            "supporting_activity_item"                 
                        ]
                                    

            for field in fields_to_update:
                new_value = validated_data.get(field)     
                                    
                  
                if new_value is not None and getattr(instance, field) != new_value:
                    # date timezone validation
                #    Time zone from request and  +2 and +3 handleing 

                    # if field =='date':
                        # new_value = validate_and_convert_to_utc(new_value)
                   
                    #end date timezone validation
                        
                    
                    setattr(instance, field, new_value)
                    updated = True

            if updated:
                instance.save()
                
            return instance
    
    
    
    
    
        def create(self, validated_data):
            return all_models.Survey.objects.create(**validated_data)

