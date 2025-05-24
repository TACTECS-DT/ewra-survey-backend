function  CalcQuestionsRes() {

    let csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    if (!csrfToken) {
        alert("CSRF token not found. Request cannot proceed.");
        return; 
    }
        let record_id =$("#record_id").val()
        if (!record_id){
            alert("record id not set")
        }
        $.ajax({
            url: "/api/CalcQuestionsRes/", 
            type: "POST",     
            headers: { "X-CSRFToken": csrfToken },  

            contentType: "application/json",
            data: JSON.stringify({ survey_id: record_id }), 
            success: function (response) {
                if (response.success) {
                    location.reload(); 
                } else {
                    alert("Error: " + (response.error || "Unknown error"));
                }
            },
            error: function (xhr) {
                alert("Request failed: " + xhr.responseText);
            }
        });
    }