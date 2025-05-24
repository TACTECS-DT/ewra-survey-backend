
$(document).ready(function () {
      

$("#id_affiliate").change(function () {
    var affiliateId = $(this).val();

    if (affiliateId) {
        $.ajax({
            url: "/get_need_center_from_affiliate/",
            data: { 'affiliate_id': affiliateId },
            dataType: 'json',
            success: function (data) {
                
                // Convert boolean value to checkbox checked state
                if (data.need_center === true || data.need_center === "true") {
                    $("#need_center_related").prop("checked", true).trigger("change");
                } else {
                    $("#need_center_related").prop("checked", false).trigger("change");
               
                }
            }
        });
    } else {
        $("#need_center_related").prop("checked", false);
    }
});

// Trigger the affiliate change event on page load to set the initial data if available
if ($("#id_affiliate").val()) {
    $("#id_affiliate").change();
}

})