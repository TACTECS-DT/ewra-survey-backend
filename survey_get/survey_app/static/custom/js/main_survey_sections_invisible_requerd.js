$(document).ready(function() {

    toggleFields();
 

    $('#id_activity_type_related').change(function() {
        toggleFields();
    });

    function toggleFields() {
  
  

        
      if ( $("#id_activity_type_related").text().trim() == 'رئيسى') {
        $('#id_activity_type').closest("div").show();
        $('#id_activity_type').prop('required', true);
    } else {

        $('#id_activity_type').closest("div").hide();
        $('#id_activity_type').prop('required', false);
    }




    }




});
