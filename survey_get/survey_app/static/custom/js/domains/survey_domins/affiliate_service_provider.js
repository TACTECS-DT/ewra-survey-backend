$(document).ready(function () {

    function affiliate_service_provider_domain() {
        var service_provider = $("#id_service_provider").val();
        var selected_affiliate = $("#id_affiliate").val();

        if (service_provider) {
            $.ajax({
                url: "/affiliate_service_provider_domain/",
                data: { 'service_provider': service_provider },
                dataType: 'json',
                success: function (data) {
                    var id_affiliateDropdown = $("#id_affiliate");
                    id_affiliateDropdown.empty();
                    id_affiliateDropdown.append('<option value="">---------</option>');

                    $.each(data, function (index, item) {
                        var selected = item.id == selected_affiliate ? "selected" : "";
                        id_affiliateDropdown.append(`<option value="${item.id}" ${selected}>${item.name}</option>`);
                    });
                }
            });
        } else {
            $("#id_affiliate").empty().append('<option value="">---------</option>');
        }
    }

    // On page load, fetch main activities for the current record
    affiliate_service_provider_domain();

    // Update when entity_type is changed
    $("#id_service_provider").change(affiliate_service_provider_domain);
});