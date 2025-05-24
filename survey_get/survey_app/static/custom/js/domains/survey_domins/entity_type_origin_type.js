$(document).ready(function () {
    function entity_type_origin_type_survey_domain() {
        var origin_type = $("#id_origin_type").val();
        var selectedMainActivity = $("#id_main_activity").val();

        if (origin_type) {
            $.ajax({
                url: "/entity_type_origin_type_survey_domain/",
                data: { 'origin_type': origin_type },
                dataType: 'json',
                success: function (data) {
                    var mainActivityDropdown = $("#id_main_activity");
                    mainActivityDropdown.empty();
                    mainActivityDropdown.append('<option value="">---------</option>');

                    $.each(data, function (index, item) {
                        var selected = item.id == selectedMainActivity ? "selected" : "";
                        mainActivityDropdown.append(`<option value="${item.id}" ${selected}>${item.name}</option>`);
                    });
                }
            });
        } else {
            $("#id_main_activity").empty().append('<option value="">---------</option>');
        }
    }

    // On page load, fetch main activities for the current record
    entity_type_origin_type_survey_domain();

    // Update when origin_type is changed
    $("#id_origin_type").change(entity_type_origin_type_survey_domain);
});