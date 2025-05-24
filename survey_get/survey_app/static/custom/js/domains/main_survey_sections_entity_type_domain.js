$(document).ready(function () {
    function fetchMainSurveySectionEType() {
        var entityType = $("#id_entity_type").val();
        var id_main_survey_sections = $("#id_main_survey_sections").val();

        if (entityType) {
            $.ajax({
                url: "/main_survey_sections_entity_type_domain/",
                data: { 'entity_type': entityType },
                dataType: 'json',
                success: function (data) {
                    var main_survey_sectionsDropdown = $("#id_main_survey_sections");
                    main_survey_sectionsDropdown.empty();
                    main_survey_sectionsDropdown.append('<option value="">---------</option>');

                    $.each(data, function (index, item) {
                        var selected = item.id == id_main_survey_sections ? "selected" : "";
                        main_survey_sectionsDropdown.append(`<option value="${item.id}" ${selected}>${item.name}</option>`);
                    });
                }
            });
        } else {
            $("#id_main_survey_sections").empty().append('<option value="">---------</option>');
        }
    }

    // On page load, fetch main activities for the current record
    fetchMainSurveySectionEType();

    // Update when entity_type is changed
    $("#id_entity_type").change(fetchMainSurveySectionEType);
});