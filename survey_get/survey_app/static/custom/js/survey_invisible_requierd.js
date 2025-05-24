$(document).ready(function() {

    // Initial check on page load to hide/show elements based on initial field values
    toggleFields();

    // Watch for changes in fields to dynamically adjust visibility and required attributes
    $('#id_service_provider').change(function() {
        toggleFields();
    });

    $('#id_affiliate').change(function() {
        toggleFields();
    });

    $('#need_center_related').change(function() {
        toggleFields();
    });

    $('#id_origin_type').change(function() {
        toggleFields();
    });

    $('#id_main_activity').change(function() {
        toggleFields();
    });

    $('#id_activity_type').change(function() {
        toggleFields();
    });

    $('#id_activity_type_related').change(function() {
        toggleFields();
    });

    $('#id_activity_item').change(function() {
        toggleFields();
    });

    $('#id_supporting_activity_item').change(function() {
        toggleFields();
    });

    $('#id_supporting_main_survey_sections').change(function() {
        toggleFields();
    });

    // Function to handle visibility and required attributes based on conditions
    function toggleFields() {
  
        if ($('#id_service_provider').val()) {
            $('#id_affiliate').prop('required', true);
            $('#id_affiliate').closest("div").show();
        } else {
            $('#id_affiliate').prop('required', false);
            $('#id_affiliate').closest("div").hide();
        }
     


        if ($('#id_affiliate').val() &&$  ('#id_service_provider').val()) {
            $('#need_center_related').closest("div").show();
            $('#id_affiliate_entity_type_related').closest("div").show();
            $('#id_main_activity').closest("div").show();
            $('#id_origin_type').closest("div").show();
       
        } else {
            $('#need_center_related').closest("div").hide();
            $('#id_affiliate_entity_type_related').closest("div").hide();
            $('#id_main_activity').closest("div").hide();
            $('#id_origin_type').closest("div").hide();
        }

        
      if ($('#need_center_related').prop('checked')) {


        $('#id_center').closest("div").show();
        $('#id_center').prop('required', true);
    } else {

        $('#id_center').closest("div").hide();
        $('#id_center').prop('required', false);
    }

   
 
        
      if ($('#id_main_activity').val()) {

        $('#id_activity_type_related').closest("div").show();
        $('#id_activity_item').closest("div").show();
        $('#id_main_survey_sections').closest("div").show();
        $('#id_supporting_activity_item').closest("div").show();
        $('#id_supporting_main_survey_sections').closest("div").show();
    } else {

        $('#id_activity_type_related').closest("div").hide();
        $('#id_activity_item').closest("div").hide();
        $('#id_main_survey_sections').closest("div").hide();
        $('#id_supporting_activity_item').closest("div").hide();
        $('#id_supporting_main_survey_sections').closest("div").hide();
    }

   
 



    if ( $("#id_activity_type_related").text().trim() == 'رئيسى') {

        $('#id_activity_type').closest("div").show();
        $('#id_activity_type').prop('required', true);

        $('#id_activity_item').closest("div").show();
        $('#id_activity_item').prop('required', true);

        $('#id_main_survey_sections').closest("div").show();
        $('#id_main_survey_sections').prop('required', true);


    } else {

        $('#id_activity_type').closest("div").hide();
        $('#id_activity_type').prop('required', false);

        $('#id_activity_item').closest("div").hide();
        $('#id_activity_item').prop('required', false);


        $('#id_main_survey_sections').closest("div").hide();
        $('#id_main_survey_sections').prop('required', false);


    }




    if ( $("#id_activity_type_related").text().trim() == 'داعم') {

        $('#id_supporting_activity_item').closest("div").show();
        $('#id_supporting_activity_item').prop('required', true);

        $('#id_supporting_main_survey_sections').closest("div").show();
        $('#id_supporting_main_survey_sections').prop('required', true);

    } else {


        $('#id_supporting_activity_item').closest("div").hide();
        $('#id_supporting_activity_item').prop('required', false);


        $('#id_supporting_main_survey_sections').closest("div").hide();
        $('#id_supporting_main_survey_sections').prop('required', false);


    }






    if ( $("#id_activity_type").val()) {

        $('#id_activity_item').closest("div").show();
        $('#id_activity_item').prop('required', true);

        $('#id_main_survey_sections').closest("div").show();
        $('#id_main_survey_sections').prop('required', true);


    } else {

        $('#id_activity_item').closest("div").hide();
        $('#id_activity_item').prop('required', false);

        $('#id_main_survey_sections').closest("div").hide();
        $('#id_main_survey_sections').prop('required', false);

    }



    if ( $("#id_activity_item").val()) {
    
        $('#id_main_survey_sections').closest("div").show();
        $('#id_main_survey_sections').prop('required', true);

    } else {

        $('#id_main_survey_sections').closest("div").hide();
        $('#id_main_survey_sections').prop('required', false);

    }





    if ( $("#id_supporting_activity_item").val()) {
    
        $('#id_supporting_main_survey_sections').closest("div").show();
        $('#id_supporting_main_survey_sections').prop('required', true);

    } else {

        $('#id_supporting_main_survey_sections').closest("div").hide();
        $('#id_supporting_main_survey_sections').prop('required', false);

    }






    // end

    }

});
