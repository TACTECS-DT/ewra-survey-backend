$(document).ready(function () {
    var originTypeSelect = $('#id_origin_type');
    var activityTypeSelect = $('#id_activity_type');
    var mainSurveySectionsSelect = $('#id_main_survey_sections');

    // Function to update main_survey_sections
    function updateMainSurveySections_domin() {
        var originType = originTypeSelect.val();
        var activityType = activityTypeSelect.val();
        var oldMainSurveySectionValue = mainSurveySectionsSelect.val(); // Store the old value

        if (originType && activityType) {
            $.ajax({
                url: "/get_survey_main_survey_sections_domain/",
                data: {
                    'origin_type': originType,
                    'activity_type': activityType
                },
                success: function (data) {
                    mainSurveySectionsSelect.empty().append(new Option("Select Main Survey Section", ""));
                    $.each(data, function (index, section) {
                        mainSurveySectionsSelect.append(new Option(section.name, section.id));

                        // If the old value exists, select it again
                        if (section.id == oldMainSurveySectionValue) {
                            mainSurveySectionsSelect.val(oldMainSurveySectionValue);
                        }
                    });
                }
            });
        }
    }

    // When origin_type or activity_type changes, update main_survey_sections
    originTypeSelect.change(updateMainSurveySections_domin);
    activityTypeSelect.change(updateMainSurveySections_domin);

    // Initialize on page load
    if (originTypeSelect.val() && activityTypeSelect.val()) {
        updateMainSurveySections_domin();
    }
});
