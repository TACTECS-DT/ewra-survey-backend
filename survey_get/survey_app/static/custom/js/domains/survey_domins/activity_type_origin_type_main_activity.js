
$(document).ready(function () {
    

    // Handle origin_type selection change
    var mainActivitySelect = $('#id_main_activity');
    var activityTypeSelect = $('#id_activity_type');
    var origin_typeSelect = $('#id_origin_type');
    var oldMainActivityValue = mainActivitySelect.val(); // Store the old value

    // When origin_type changes, update main_activity
    origin_typeSelect.change(function () {
        var origin_type = $(this).val();

        if (origin_type) {
            $.ajax({
                url: "/main_activity_origin_type_domain/",
                data: { 'origin_type': origin_type },
                success: function (data) {
                    mainActivitySelect.empty().append(new Option("Select Main Activity", ""));
                    $.each(data, function (index, activity) {
                        mainActivitySelect.append(new Option(activity.name, activity.id));
                
                   // If the old value exists in the new data, select it
                   if (activity.id == oldMainActivityValue) {
                        mainActivitySelect.val(oldMainActivityValue);
                        found = true;
                    }
                
                
                    });

                    // Trigger main_activity change if it's already selected
                    if (mainActivitySelect.val()) {
                        updateActivityType();
                    }
                }
            });
        }
    });

    // When main_activity changes, update activity_type
    mainActivitySelect.change(function () {
        updateActivityType();
    });

    // Function to update activity_type based on main_activity and origin_type
    function updateActivityType() {
        var mainActivity = mainActivitySelect.val();
        var origin_type = origin_typeSelect.val();
        var oldActivityTypeValue = activityTypeSelect.val(); // Store the old value

        if (mainActivity && origin_type) {
            $.ajax({
                url: "/get_main_activity_origin_type_activity_type_domain/",
                data: {
                    'main_activity': mainActivity,
                    'origin_type': origin_type
                },
                success: function (data) {
                    activityTypeSelect.empty().append(new Option("Select Activity Type", ""));
                    $.each(data, function (index, activityType) {
                        activityTypeSelect.append(new Option(activityType.name, activityType.id));


// If the old value exists in the new data, select it
if (activityType.id == oldActivityTypeValue) {
                        activityTypeSelect.val(oldActivityTypeValue);
                        found = true;
                    }


                    });
                }
            });
        }
    }

    // Initialize main_activity if origin_type has value already
    if (origin_typeSelect.val()) {
        origin_typeSelect.change();
    }

    // Initialize activity_type if both main_activity and origin_type are selected
    if (mainActivitySelect.val() && origin_typeSelect.val()) {
        updateActivityType();
    }

    // Trigger change events for origin_type and main_activity on page load to load the initial data
    if ($("#id_origin_type").val()) {
        origin_typeSelect.change();
    }

    if ($("#id_main_activity").val()) {
        mainActivitySelect.change();
    }
});


