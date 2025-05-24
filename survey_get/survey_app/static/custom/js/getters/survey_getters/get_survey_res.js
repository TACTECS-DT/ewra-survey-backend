$(document).ready(function () {
    var surveyId = $('#record_id'); // Assuming this is the survey ID field

    function updateSurveyFields() {
        var survey_id = surveyId.val();
       
        if (survey_id) {
            $.ajax({
                url: "/get_survey_res_data/",
                data: { 'survey_id': survey_id },
                success: function (data) {
                    if (data) {
                        var percentage = (parseFloat(data.visit_result_percntage) * 100).toFixed(4) + '%';
               
                        $('#full_mark').text(data.full_mark);
                        $('#visit_result').text(data.visit_result);
                        $('#visit_result_percntage').text(percentage);
                        // $('#visit_result_percntage').text(data.visit_result_percntage);
                        $('#questions_added').prop('checked', data.questions_added);
                        $('#visit_result_done').prop('checked', data.visit_result_done);
                    }
                }
            });
        }
    }

    // Trigger AJAX call when survey selection changes
    surveyId.change(updateSurveyFields);

    // Initialize on page load
    if (surveyId.val()) {
        updateSurveyFields();
    }
});
