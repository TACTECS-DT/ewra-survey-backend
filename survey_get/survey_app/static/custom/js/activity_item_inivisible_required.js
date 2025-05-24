$(document).ready(function() {

    toggleFields();
 
    $('#id_affiliate').change(function() {
        toggleFields();
    });

    $('#need_center_related').change(function() {
        toggleFields();
    });

    $('#id_activity_type_related').change(function() {
        toggleFields();
    });

    function toggleFields() {
  
  

        if ($('#id_affiliate').val()) {
            $('#need_center_related').closest("div").show();
        } else {
            $('#need_center_related').closest("div").hide();
        }

        
      if ($('#need_center_related').prop('checked')) {


        $('#id_center').closest("div").show();
        $('#id_center').prop('required', true);
    } else {

        $('#id_center').closest("div").hide();
        $('#id_center').prop('required', false);
    }

        
      if ( $("#id_activity_type_related").text().trim() == 'رئيسى') {
        $('#id_branch').closest("div").show();
        $('#id_branch').prop('required', true);
    } else {

        $('#id_branch').closest("div").hide();
        $('#id_branch').prop('required', false);
    }




    }




});
