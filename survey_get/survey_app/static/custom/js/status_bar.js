function changeState(newState) {
    console.log(newState,"-> newState")
    let survey_id = document.getElementById("record_id").value
    if (!survey_id){
        alert("Cannot get survey id")
    }
    // Example: Sending a request to change the state
    fetch('/update_state/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Ensure CSRF token is included
        },
        body: JSON.stringify({
            
            new_state: newState ,
            survey_id: survey_id ,


        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Refresh page to update status
        } else {
            console.log(data)
            alert('فشل في تحديث الحالة');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to get CSRF Token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
