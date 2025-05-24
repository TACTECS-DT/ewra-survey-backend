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
        } else {
            $('#need_center_related').closest("div").hide();
        }


// center   
      // Center visibility based on need_center_related and other conditions
//       if ($('#need_center_related').prop('checked') && $('#id_affiliate').val() && $('#id_service_provider').val()) {
//         $('#id_center').closest("div").show();
//     } else {
//         $('#id_center').closest("div").hide();
//     }


//         if ($('#need_center_related').prop('checked')  ) {
//             $('#id_center').prop('required', true);
//         } else {
//             $('#id_center').prop('required', false);
//         }
// ///////////////



    }




});
