import { map, Place } from '../map_view.js'; 



$(document).ready(function () {


    if (L.DomUtil.get('map') !== null) {
        L.DomUtil.get('map')._leaflet_id = null;
    }
    
    

    function get_activity_items_geo_report() {
        $.ajax({
            url: "/get_activity_items_geo_report/",
            dataType: "json",
            success: function (data) {
                if (data && data.activity_items) {
                    createPlacesFromSurveys(data.activity_items);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error fetching activity items:", error);
            }
        });
    }

    function createPlacesFromSurveys(activityItems) {
        let places = [];

        activityItems.forEach(item => {
            let avgResult = parseFloat(item.average_result) || 0; // Ensure it's a number
            let average_result_percetange = parseFloat(item.average_result_percetange *100) || 0; // Ensure it's a number

            // Base popup content
                let popupContent ='' ;

            // Append each survey's details
            item.surveys.forEach(survey => {
                
                popupContent+= `<hr><b>Survey Name:</b> ${survey.survey_name}<br>
                                 <b>Visit Result:</b> ${survey.visit_result}<br>
                                 <b>Visit Percentage:</b> ${survey.visit_result_percentage*100}%
                               <hr>`;
            });

            let place = new Place(
                item.name,       // Activity item name as title
                item.latitude,   // Activity Item latitude
                item.longitude,  // Activity Item longitude
                popupContent,    // Popup content
                // avgResult  ,
                average_result_percetange    
                    );
            places.push(place);
        });

        console.log(places, "places");

        // Add all places to the map
        places.forEach(place => place.addToMap(map));
    }

    // Initialize AJAX Call on Page Load
    get_activity_items_geo_report();
});
