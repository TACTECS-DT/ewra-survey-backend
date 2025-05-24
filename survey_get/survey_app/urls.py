
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls import handler404, handler500, handler403, handler400
from . import login
from .all_views.permissions import permessions_list_page , permissions_form_page ,check_and_create_permissions

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .all_apis  import (
     # test
     TestGETAPIView,
     TestPOSTAPIView,
     TestPATCHGETAPIView,
     TestDELETEAPIView,
     
     # Activity Item
    ActivityItemGETAPIView ,
     ActivityItemPATCHGETAPIView,
     ActivityItemPOSTAPIView,
     ActivityItemDELETEAPIView,
     
     # Governorate
     GovernorateGETAPIView ,
     GovernoratePATCHGETAPIView,
     GovernoratePOSTAPIView,
     GovernorateDELETEAPIView,
     
     # center
     CenterGETAPIView ,
     CenterPATCHGETAPIView,
     CenterPOSTAPIView,
     CenterDELETEAPIView,
     
     # ServiceProvider
     ServiceProviderPATCHGETAPIView,
     ServiceProviderGETAPIView,
     ServiceProviderPOSTAPIView,
     ServiceProviderDELETEAPIView,
     
     
     # affiliates
     AffiliateDELETEAPIView ,
     AffiliateGETAPIView,
     AffiliatePATCHGETAPIView,
     AffiliatePOSTAPIView,
          
     # branches
     BranchGETAPIView,
     BranchPATCHGETAPIView,
     BranchPOSTAPIView,
     BranchDELETEAPIView,
     
     # MainActivity
     MainActivityPATCHGETAPIView ,
     MainActivityGETAPIView,
     MainActivityPOSTAPIView,
     MainActivityDELETEAPIView,
 
     # activity Type
     ActivityTypeDELETEAPIView ,
     ActivityTypePATCHGETAPIView,
     ActivityTypeGETAPIView,
     ActivityTypePOSTAPIView,

 
# main survey sections
 MainSurveySectionDELETEAPIView,
MainSurveySectionPATCHGETAPIView,
MainSurveySectionGETAPIView,
MainSurveySectionPOSTAPIView,

# sub survey sections
 
SubSurveySectionGETAPIView,
SubSurveySectionPATCHGETAPIView,
SubSurveySectionPOSTAPIView,
SubSurveySectionDELETEAPIView,
 
 
#  Question Bank
QuestionBankGETAPIView,

QuestionBankPATCHGETAPIView,
QuestionBankPOSTAPIView,
QuestionBankDELETEAPIView,

SurveyGETAPIView,
SurveyPATCHGETAPIView,
SurveyPOSTAPIView,
SurveyDELETEAPIView,
)

urlpatterns = [
    
# JTW main
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
# --------------------REST apis--------------------------------


     # test        
      path('api/test/', TestGETAPIView.as_view(), name='api-test-get'),
      path('api/test/new/', TestPOSTAPIView.as_view(), name='api-test-post'),
      path('api/test/<int:pk>/', TestPATCHGETAPIView.as_view(), name='api-test-patch-get'),
     #  will replace it with most new 
     #  path('api/test/<int:pk>/delete/', TestDELETEAPIView.as_view(), name='api-test-delete'), 



   # Activity Item        
      path('api/activity-item/', ActivityItemGETAPIView.as_view(), name='api-activity-item-get'),
     
      path('api/activity-item/new/', ActivityItemPOSTAPIView.as_view(), name='api-activity-item-post'),
      
      path('api/activity-item/<int:pk>/', ActivityItemPATCHGETAPIView.as_view(), name='api-activity-item-get-patch'),
      
     path('api/activity-item/delete/', ActivityItemDELETEAPIView.as_view(), name='api-activity-item-delete'),


   #Governorate       
      path('api/governorate/', GovernorateGETAPIView.as_view(), name='api-governorate-get'),
      path('api/governorate/<int:pk>/', GovernoratePATCHGETAPIView.as_view(), name='api-governorate-get-patch'),
      path('api/governorate/new/', GovernoratePOSTAPIView.as_view(), name='api-governorate-new'),
    
     path('api/governorate/delete/', GovernorateDELETEAPIView.as_view(), name='api-governorate-delete'),


   #center       
      path('api/center/', CenterGETAPIView.as_view(), name='api-center-get'),
      path('api/center/<int:pk>/', CenterPATCHGETAPIView.as_view(), name='api-center-get-patch'),
      path('api/center/new/', CenterPOSTAPIView.as_view(), name='api-center-new'),
    
     path('api/center/delete/', CenterDELETEAPIView.as_view(), name='api-center-delete'),


   #service-provider       
      path('api/service-provider/', ServiceProviderGETAPIView.as_view(), name='api-service-provider-get'),
      path('api/service-provider/<int:pk>/', ServiceProviderPATCHGETAPIView.as_view(), name='api-service-provider-get-patch'),
      path('api/service-provider/new/', ServiceProviderPOSTAPIView.as_view(), name='api-service-provider-new'),
    
     path('api/service-provider/delete/', ServiceProviderDELETEAPIView.as_view(), name='api-service-provider-delete'),
     
     
# affiliate

      path('api/affiliate/', AffiliateGETAPIView.as_view(), name='api-affiliate-get'),
      path('api/affiliate/<int:pk>/', AffiliatePATCHGETAPIView.as_view(), name='api-affiliate-get-patch'),
      path('api/affiliate/new/', AffiliatePOSTAPIView.as_view(), name='api-affiliate-new'),
    
     path('api/affiliate/delete/', AffiliateDELETEAPIView.as_view(), name='api-affiliate-delete'),
     
  #branches       
      path('api/branch/', BranchGETAPIView.as_view(), name='api-branch-get'),
      path('api/branch/<int:pk>/', BranchPATCHGETAPIView.as_view(), name='api-branch-get-patch'),
      path('api/branch/new/', BranchPOSTAPIView.as_view(), name='api-branch-new'),
     path('api/branch/delete/', BranchDELETEAPIView.as_view(), name='api-branch-delete'),

     
  #MainActivity       
      path('api/main-activity/',MainActivityGETAPIView.as_view(), name='api-main-activity-get'),
      path('api/main-activity/<int:pk>/', MainActivityPATCHGETAPIView.as_view(), name='api-main-activity-get-patch'),
      path('api/main-activity/new/', MainActivityPOSTAPIView.as_view(), name='api-main-activity-new'),
      path('api/main-activity/delete/', MainActivityDELETEAPIView.as_view(), name='api-main-activity-delete'),


  #activity-type       
      path('api/activity-type/', ActivityTypeGETAPIView.as_view(), name='api-activity-type-get'),
      path('api/activity-type/<int:pk>/', ActivityTypePATCHGETAPIView.as_view(), name='api-activity-type-get-patch'),
      path('api/activity-type/new/', ActivityTypePOSTAPIView.as_view(), name='api-activity-type-new'),
     path('api/activity-type/delete/', ActivityTypeDELETEAPIView.as_view(), name='api-activity-type-delete'),

     
 #main-survey-sections       
      path('api/main-survey-section/', MainSurveySectionGETAPIView.as_view(), name='api-main-survey-section-get'),
      path('api/main-survey-section/<int:pk>/', MainSurveySectionPATCHGETAPIView.as_view(), name='api-main-survey-section-get-patch'),
      path('api/main-survey-section/new/', MainSurveySectionPOSTAPIView.as_view(), name='api-main-survey-section-new'),
     path('api/main-survey-section/delete/', MainSurveySectionDELETEAPIView.as_view(), name='api-main-survey-section-delete'),


# sub survey sections
      path('api/sub-survey-section/', SubSurveySectionGETAPIView.as_view(), name='api-sub-survey-section-get'),
      path('api/sub-survey-section/<int:pk>/', SubSurveySectionPATCHGETAPIView.as_view(), name='api-sub-survey-section-get-patch'),
      path('api/sub-survey-section/new/', SubSurveySectionPOSTAPIView.as_view(), name='api-sub-survey-section-new'),
     path('api/sub-survey-section/delete/', SubSurveySectionDELETEAPIView.as_view(), name='api-sub-survey-section-delete'),



 #question-bankes       
      path('api/question-bank/', QuestionBankGETAPIView.as_view(), name='api-question-bank-get'),
      path('api/question-bank/<int:pk>/', QuestionBankPATCHGETAPIView.as_view(), name='api-question-bank-get-patch'),
      path('api/question-bank/new/', QuestionBankPOSTAPIView.as_view(), name='api-question-bank-new'),
     path('api/question-bank/delete/', QuestionBankDELETEAPIView.as_view(), name='api-question-bank-delete'),






 #survey    
      path('api/survey/', SurveyGETAPIView.as_view(), name='api-survey-get'),
      path('api/survey/<int:pk>/', SurveyPATCHGETAPIView.as_view(), name='api-survey-get-patch'),
      path('api/survey/new/', SurveyPOSTAPIView.as_view(), name='api-survey-new'),
      path('api/survey/delete/', SurveyDELETEAPIView.as_view(), name='api-survey-delete'),














# -----------------------------------------------

#  home page
    path('', views.home_page, name='home'),
           
      path('login/', login.CustomLoginView.as_view(template_name='login/login.html'), name='login'),
           
      path('logout/', login.logout_page, name='logout'),     
     #  path('api/jwt/logout/', login.jwt_logout_page, name='jwt-logout'),     
          
             
# permissions
     path('permissions/', permessions_list_page, name='permissions-list'),
          path("permessions/<int:pk>/", permissions_form_page, name="permissions-form"),
          path("permessions/check-create/", check_and_create_permissions, name="permissions-check-create"),


# delete_attchment_file
    path('delete_attchment_file/<int:file_id>/', views.delete_attchment_file, name='delete_attchment_file'),




     
# governorates
     path('governorates/', views.governorates_list_page, name='governorates-list'),
     path('governorates/<int:pk>/', views.governorates_form_page, name='governorates-form'),
     
    path('governorates/<int:pk>/delete/', views.governorates_delete_page, name='governorates-delete'),
      
      path('governorates/new/', views.governorates_create_page, name='governorates-create'),

             
# centers
     path('centers/', views.centers_list_page, name='centers-list'),
     path('centers/<int:pk>/', views.centers_form_page, name='centers-form'),
     
    path('centers/<int:pk>/delete/', views.centers_delete_page, name='centers-delete'),
      
      path('centers/new/', views.centers_create_page, name='centers-create'),
             
# service-providers
     path('service-providers/', views.service_provider_list_page, name='service-providers-list'),
     path('service-providers/<int:pk>/', views.service_provider_form_page, name='service-providers-form'),
     
    path('service-providers/<int:pk>/delete/', views.service_provider_delete_page, name='service-providers-delete'),
      
      path('service-providers/new/', views.service_provider_create_page, name='service-providers-create'),

             
# affiliates
     path('affiliates/', views.affiliates_list_page, name='affiliates-list'),
     path('affiliates/<int:pk>/', views.affiliates_form_page, name='affiliates-form'),
     
    path('affiliates/<int:pk>/delete/', views.affiliates_delete_page, name='affiliates-delete'),
      
      path('affiliates/new/', views.affiliates_create_page, name='affiliates-create'),
             

     
             
# Branch
     path('branches/', views.branches_list_page, name='branches-list'),
     path('branches/<int:pk>/', views.branches_form_page, name='branches-form'),
     
    path('branches/<int:pk>/delete/', views.branches_delete_page, name='branches-delete'),
      
      path('branches/new/', views.branches_create_page, name='branches-create'),

             
# MainActivity
     path('main-activity/', views.main_activity_list_page, name='main-activity-list'),
     path('main-activity/<int:pk>/', views.main_activity_form_page, name='main-activity-form'),
     
    path('main-activity/<int:pk>/delete/', views.main_activity_delete_page, name='main-activity-delete'),
      
      path('main-activity/new/', views.main_activity_create_page, name='main-activity-create'),
             
# ActivityType

     path('activity-types/', views.activity_types_list_page, name='activity-types-list'),
     path('activity-types/<int:pk>/', views.activity_types_form_page, name='activity-types-form'),
     
    path('activity-types/<int:pk>/delete/', views.activity_types_delete_page, name='activity-types-delete'),
      
      path('activity-types/new/', views.activity_types_create_page, name='activity-types-create'),



# ActivityItems

     path('activity-items/', views.activity_items_list_page, name='activity-items-list'),
     path('activity-items/<int:pk>/', views.activity_items_form_page, name='activity-items-form'),
     
    path('activity-items/<int:pk>/delete/', views.activity_items_delete_page, name='activity-items-delete'),
      
      path('activity-items/new/', views.activity_items_create_page, name='activity-items-create'),
     

# main-survey-sections


     path('main-survey-sections/', views.main_survey_sections_list_page, name='main-survey-sections-list'),
     path('main-survey-sections/<int:pk>/', views.main_survey_sections_form_page, name='main-survey-sections-form'),
     
    path('main-survey-sections/<int:pk>/delete/', views.main_survey_sections_delete_page, name='main-survey-sections-delete'),
      
      path('main-survey-sections/new/', views.main_survey_sections_create_page, name='main-survey-sections-create'),

# sub-survey-sections


     path('sub-survey-sections/', views.sub_survey_sections_list_page, name='sub-survey-sections-list'),
     path('sub-survey-sections/<int:pk>/', views.sub_survey_sections_form_page, name='sub-survey-sections-form'),
     
    path('sub-survey-sections/<int:pk>/delete/', views.sub_survey_sections_delete_page, name='sub-survey-sections-delete'),
      
      path('sub-survey-sections/new/', views.sub_survey_sections_create_page, name='sub-survey-sections-create'),

# QuestionBank

    path('question-bank/', views.question_bank_list_page, name='question-bank-list'),
     path('question-bank/<int:pk>/', views.question_bank_form_page, name='question-bank-form'),
     
    path('question-bank/<int:pk>/delete/', views.question_bank_delete_page, name='question-bank-delete'),
      
      path('question-bank/new/', views.question_bank_create_page, name='question-bank-create'),
    
             
# survey
     path('survey/', views.survey_list_page, name='survey-list'),
     path('survey/<int:pk>/', views.survey_form_page, name='survey-form'),
     
    path('survey/<int:pk>/delete/', views.survey_delete_page, name='survey-delete'),
      
      path('survey/new/', views.survey_create_page, name='survey-create'),

            
# users
     path('users/', views.users_list_page, name='users-list'),
     path('users/<int:pk>/', views.user_form_page, name='users-form'),
     
    path('users/<int:pk>/delete/', views.users_delete_page, name='users-delete'),
      
      path('users/new/', views.users_create_page, name='users-create'),


# reports
     

     path('activity-items-geo/', views.activity_items_geo, name='activity_items_geo'),
     path('get_activity_items_geo_report/', views.get_activity_items_geo_report, name='get_activity_items_geo_report'),

     path('survey-reports/', views.survey_reports_view, name='survey_reports'),
     path('reports/', views.all_reports_view, name='reports'),

# getters
     
     path('update_state/', views.update_state, name='update_state'),

     path('get_activity_type_from_main_activity/', views.get_activity_type_from_main_activity, name='get_activity_type_from_main_activity'),

     path('get_service_provider_from_affiliate/', views.get_service_provider_from_affiliate, name='get_service_provider_from_affiliate'),

     path('get_need_center_from_affiliate/', views.get_need_center_from_affiliate, name='get_need_center_from_affiliate'),
     
     path('get_entity_type_from_affiliate/', views.get_entity_type_from_affiliate, name='get_entity_type_from_affiliate'),


     path('api/add_Q/', views.add_questions, name='add_questions'),
     path('api/CalcQuestionsRes/', views.calc_questions_res, name='CalcQuestionsRes'),


     path('get_survey_res_data/', views.get_survey_res_data, name='get_survey_res_data'),
     path('api/get_survey_report_data/', views.get_survey_report_data, name='get_survey_report_data'),



# domains
     path('main_activity_entity_type_domain/', views.main_activity_entity_type_domain, name='main_activity_entity_type_domain'),
     
     path('get_main_activity_entity_type_activity_type_domain/', views.get_main_activity_entity_type_activity_type_domain, name='get_main_activity_entity_type_activity_type_domain'),

     
     path('main_survey_sections_entity_type_domain/', views.main_survey_sections_entity_type_domain, name='main_survey_sections_entity_type_domain'),


     path('affiliate_service_provider_domain/', views.affiliate_service_provider_domain, name='affiliate_service_provider_domain'),



     path('entity_type_origin_type_survey_domain/', views.entity_type_origin_type_survey_domain, name='entity_type_origin_type_survey_domain'),



     path('main_activity_origin_type_domain/', views.main_activity_origin_type_domain, name='main_activity_origin_type_domain'),



     path('get_main_activity_origin_type_activity_type_domain/', views.get_main_activity_origin_type_activity_type_domain, name='get_main_activity_origin_type_activity_type_domain'),

     path('get_survey_activity_item_domain/', views.get_survey_activity_item_domain, name='get_survey_activity_item_domain'),
     
     path('get_survey_main_survey_sections_domain/', views.get_survey_main_survey_sections_domain, name='get_survey_main_survey_sections_domain'),
     
     
     path('get_survey_supporting_activity_item_domain/', views.get_survey_supporting_activity_item_domain, name='get_survey_supporting_activity_item_domain'),
  
  
     path('get_supporting_main_survey_sections_domain/', views.get_supporting_main_survey_sections_domain, name='get_supporting_main_survey_sections_domain'),





#    export

     path('export-model/', views.export_model_to_excel, name='export-model'),
     path('export-m2m-model/', views.export_many2many_to_excel, name='export-m2m-model'),



#    403 
     path('403/', views.forbidden_page, name='403'),
     
    #    404 
     path('404/', views.not_found_page, name='404'),
          
    #    400 
     path('400/', views.custom_400_view, name='400'),
              
    #    500 
     path('500/', views.custom_500_view, name='500'),
     


]


    

handler404 = 'survey_app.views.not_found_page'
handler500 = 'survey_app.views.custom_500_view'
handler403 = 'survey_app.views.forbidden_page'
handler400 = 'survey_app.views.custom_400_view'

