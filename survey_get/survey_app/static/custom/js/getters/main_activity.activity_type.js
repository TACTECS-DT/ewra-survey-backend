$(document).ready(function () {
      
    function get_activity_type_from_main_activity() {
        var main_activityId = $("#id_main_activity").val(); 
        if (main_activityId) {
            $.ajax({
                url: "/get_activity_type_from_main_activity/",
                data: { 'main_activityId': main_activityId },
                dataType: 'json',
                success: function (data) {
                    if (data.activity_type_name) {
                        $("#id_activity_type_related").html(`<p>${data.activity_type_name}</p>`).trigger("change");
                    } else {
                        $("#id_activity_type_related").html(`<p></p>`).trigger("change");
                    }
                }
            });
        } else {
            $("#id_activity_type_related").html(`<p></p>`).trigger("change");
        }
    }

    // Bind change event to the dropdown
    $("#id_main_activity").change(get_activity_type_from_main_activity);

    // Call function on page load only if a value is preselected
    if ($("#id_main_activity").val()) {
        get_activity_type_from_main_activity();
    }
});