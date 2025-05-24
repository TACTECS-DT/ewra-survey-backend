$(document).ready(function () {
    var originTypeSelect = $('#id_origin_type');
    var activityTypeSelect = $('#id_activity_type');
    var activityItemSelect = $('#id_activity_item');
    var affiliateSelect = $('#id_affiliate');

    // Function to update activity_item
    function survey_updateActivityItem() {

        var originType = $('#id_origin_type').val();
        var activityType = $('#id_activity_type').val();
        var affiliateId = $('#id_affiliate').val();
        var oldActivityItemValue = $('#id_activity_item').val(); // Store the old value

        if (originType && activityType && affiliateId) {
 
 
            $.ajax({
                url: "/get_survey_activity_item_domain/",
                data: {
                    'origin_type': originType,
                    'activity_type': activityType,
                    'affiliate_id': affiliateId
                },
                success: function (data) {
                    activityItemSelect.empty().append(new Option("Select Activity Item", ""));
                    $.each(data, function (index, activityItem) {
                        activityItemSelect.append(new Option(activityItem.name, activityItem.id));

                        // If the old value exists, select it again
                        if (activityItem.id == oldActivityItemValue) {
                            activityItemSelect.val(oldActivityItemValue);
                        }
                    });
                }
            });
        }
    }

    // When origin_type, activity_type, or affiliate_id changes, update activity_item
    $('#id_origin_type').change(survey_updateActivityItem);
    $('#id_activity_type').change(survey_updateActivityItem);
    $('#id_affiliate').change(survey_updateActivityItem);
  
    // Initialize on page load
    if ($('#id_origin_type').val() && $('#id_activity_type').val() && $('#id_affiliate').val()) {
        survey_updateActivityItem();
    }
});
