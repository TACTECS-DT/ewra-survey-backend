$(document).ready(function () {
      
    function get_entity_type_from_affiliate(){
        var affiliate_id = $("#id_affiliate").val(); 
        if (affiliate_id) {
            $.ajax({
                url: "/get_entity_type_from_affiliate/",
                data: { 'affiliate_id': affiliate_id },
                dataType: 'json',
                success: function (data) {
                    if (data.entity_type) {
                        $("#id_affiliate_entity_type_related").html(`<p>${data.entity_type}</p>`);
                    } else {
                        $("#id_affiliate_entity_type_related").html(`<p></p>`);
                    }
                }
            });
        } else {
            $("#id_affiliate_entity_type_related").html(`<p></p>`);
        }
    }

    // Bind change event to the dropdown
    $("#id_affiliate").change(get_entity_type_from_affiliate);

    // Call function on page load only if a value is preselected
    if ($("#id_affiliate").val()) {
        get_entity_type_from_affiliate();
    }
});