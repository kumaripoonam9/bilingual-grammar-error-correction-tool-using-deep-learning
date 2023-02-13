console.log('working')

$(document).on('submit', '#message_form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: window.location.href,
        data: {
            message: $('#message').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        }
    });
    $(".parent").load(window.location.href + " .parent");
    $(".parent").enhanceWithin(); 
    

})

$(document).ready(function () {
    setInterval(function () {
        $("#chatbox").load(window.location.href + " #chatbox");
        // $("#chatbox").enhanceWithin(); 
    }, 500)
})

$(document).ready(function () {
    setInterval(function () {
        $(".room_list").load(window.location.href + " .room_list");
        // $("#chatbox").enhanceWithin(); 
    }, 3000)
})
