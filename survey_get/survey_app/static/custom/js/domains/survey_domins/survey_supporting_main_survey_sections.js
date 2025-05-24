$(document).ready(function () {
    var originTypeSelect = $('#id_origin_type');
    var mainActivitySelect = $('#id_main_activity');
    var supportingMainSurveySectionsSelect = $('#id_supporting_main_survey_sections');

    // Function to update supporting_main_survey_sections
    function updateSupportingMainSurveySections() {
        var originType = originTypeSelect.val();
        var mainActivity = mainActivitySelect.val();
        var oldSupportingMainSurveySectionsValue = $('#id_supporting_main_survey_sections').val(); // Store old value

        if (originType && mainActivity) {
            $.ajax({
                url: "/get_supporting_main_survey_sections_domain/",
                data: {
                    'main_activity': mainActivity,
                    'origin_type': originType
                },
                success: function (data) {
                    supportingMainSurveySectionsSelect.empty().append(new Option("Select Survey Section", ""));
                    $.each(data, function (index, section) {
                        supportingMainSurveySectionsSelect.append(new Option(section.name, section.id));
                        console.log(oldSupportingMainSurveySectionsValue,'oldSupportingMainSurveySectionsValue')

                        console.log(section.id,'section.id')
                        // If the old value exists, select it again
                        if (section.id == $('#id_supporting_main_survey_sections').val() ) {
                    
                            supportingMainSurveySectionsSelect.val(oldSupportingMainSurveySectionsValue);
                        }
                    });
                }
            });
        }
    }

    // When origin_type or main_activity changes, update supporting_main_survey_sections
    originTypeSelect.change(updateSupportingMainSurveySections);
    mainActivitySelect.change(updateSupportingMainSurveySections);

    // Initialize on page load
    if (originTypeSelect.val() && mainActivitySelect.val()) {
        updateSupportingMainSurveySections();
    }
});
