
$(document).ready(function () {
      

$("#id_affiliate").change(function () {
    var affiliateId = $(this).val();

    if (affiliateId) {
        $.ajax({
            url: "/get_service_provider_from_affiliate/",
            data: { 'affiliate_id': affiliateId },
            dataType: 'json',
            success: function (data) {
                $("#id_service_provider_related").text(data.service_provider);
    
            }
        });
    } else {
        $("#id_service_provider_related").text("");
       
    }
});

// Trigger the affiliate change event on page load to set the initial data if available
if ($("#id_affiliate").val()) {
    $("#id_affiliate").change();
}

})