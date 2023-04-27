
let edited_room_name = document.getElementById("room_name_display")
let original_room_name = document.getElementById("original_room_name").textContent

let csrftoken = getCookie('csrftoken');

edited_room_name.addEventListener("input", function () {

    let new_room_name = edited_room_name.textContent
    let data = {
        'original_room_name': original_room_name,
        'edited_room_name': new_room_name,
    }

    fetch(original_room_name+'/edit_room_name/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(data),
        credentials: 'same-origin',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success: ', data)
        })
        .catch((error) => {
            console.error('My Error: ', error)
        })
}, false);


// The following function are copying from
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax

function getCookie(edited_room_name) {

    var cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, edited_room_name.length + 1) === (edited_room_name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(edited_room_name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}