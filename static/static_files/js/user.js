$('#chat-form').on('submit', function (event) {
    event.preventDefault();
    $.ajax({
        url: '/chat/',
        type: 'POST',
        data: $(this).serialize(),
        success: function (data) {
            $('.name-input').hide();
            $('.chat_input').val('');
            $('.msg_container_base').append(data);
            console.log('ok');

            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
    return false
});

function get_message() {
    $.ajax({
        url: "/messages/get/",
        type: "GET"
    })
        .done(function (data) {
            $('.msg_container_base').append(data);
            // read_message(data);
            console.log('success receive');

        })
        .fail(function (data) {
            console.log('error receive');
        })
        .always(
            setTimeout(get_message, 5000)
        )
}

function read_message(data) {
    $.ajax({
        url: "/messages/read/",
        type: "GET"
    })
        .done(function (data) {
            console.log('success receive');
        })
        .fail(function (data) {
            console.log('error receive');
        })
}


$(document).ready(get_message());

