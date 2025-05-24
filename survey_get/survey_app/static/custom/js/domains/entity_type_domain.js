$(document).ready(function () {
    function fetchMainActivities() {
        var entityType = $("#id_entity_type").val();
        var selectedMainActivity = $("#id_main_activity").val();

        if (entityType) {
            $.ajax({
                url: "/main_activity_entity_type_domain/",
                data: { 'entity_type': entityType },
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
    fetchMainActivities();

    // Update when entity_type is changed
    $("#id_entity_type").change(fetchMainActivities);
});