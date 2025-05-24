
$(document).ready(function () {


    // Handle entity_type selection change
    var mainActivitySelect = $('#id_main_activity');
    var activityTypeSelect = $('#id_activity_type');
    var entityTypeSelect = $('#id_entity_type');
    var oldMainActivityValue = mainActivitySelect.val(); // Store the old value

    // When entity_type changes, update main_activity
    entityTypeSelect.change(function () {
        var entityType = $(this).val();

        if (entityType) {
            $.ajax({
                url: "/main_activity_entity_type_domain/",
                data: { 'entity_type': entityType },
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

    // Function to update activity_type based on main_activity and entity_type
    function updateActivityType() {
        var mainActivity = mainActivitySelect.val();
        var entityType = entityTypeSelect.val();
        var oldActivityTypeValue = activityTypeSelect.val(); // Store the old value

        if (mainActivity && entityType) {
            $.ajax({
                url: "/get_main_activity_entity_type_activity_type_domain/",
                data: {
                    'main_activity': mainActivity,
                    'entity_type': entityType
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

    // Initialize main_activity if entity_type has value already
    if (entityTypeSelect.val()) {
        entityTypeSelect.change();
    }

    // Initialize activity_type if both main_activity and entity_type are selected
    if (mainActivitySelect.val() && entityTypeSelect.val()) {
        updateActivityType();
    }

    // Trigger change events for entity_type and main_activity on page load to load the initial data
    if ($("#id_entity_type").val()) {
        entityTypeSelect.change();
    }

    if ($("#id_main_activity").val()) {
        mainActivitySelect.change();
    }
});


