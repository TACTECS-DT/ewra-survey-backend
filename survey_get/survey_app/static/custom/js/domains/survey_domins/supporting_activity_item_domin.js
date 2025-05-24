$(document).ready(function () {
    var originTypeSelect = $('#id_origin_type');
    var mainActivitySelect = $('#id_main_activity');
    var affiliateSelect = $('#id_affiliate');
    var supportingActivityItemSelect = $('#id_supporting_activity_item');

    // Function to update supporting_activity_item
    function updateSupportingActivityItem() {
        var originType = originTypeSelect.val();
        var mainActivity = mainActivitySelect.val();
        var affiliateId = affiliateSelect.val();
        var oldSupportingActivityItemValue = supportingActivityItemSelect.val(); // Store old value

        if (originType && mainActivity && affiliateId) {
            $.ajax({
                url: "/get_survey_supporting_activity_item_domain/",
                data: {
                    'origin_type': originType,
                    'main_activity': mainActivity,
                    'affiliate_id': affiliateId
                },
                success: function (data) {
                    supportingActivityItemSelect.empty().append(new Option("Select Supporting Activity Item", ""));
                    $.each(data, function (index, activityItem) {
                        supportingActivityItemSelect.append(new Option(activityItem.name, activityItem.id));

                        // If the old value exists, select it again
                        if (activityItem.id == oldSupportingActivityItemValue) {
                            supportingActivityItemSelect.val(oldSupportingActivityItemValue);
                        }
                    });
                }
            });
        }
    }

    // When origin_type, main_activity, or affiliate_id changes, update supporting_activity_item
    originTypeSelect.change(updateSupportingActivityItem);
    mainActivitySelect.change(updateSupportingActivityItem);
    affiliateSelect.change(updateSupportingActivityItem);

    // Initialize on page load
    if (originTypeSelect.val() && mainActivitySelect.val() && affiliateSelect.val()) {
        updateSupportingActivityItem();
    }
});
