$(document).ready(function () {
    if (!$('.name-input')) {
        get_message()
    }
});

$('#chat-form').on('submit', function (event) {
    event.preventDefault();
    $.ajax({
        url: '/chat/',
        type: $(this).attr('method'),
        data: $(this).serialize()
    })
        .done(function (data) {
            $('.name-input').remove();
            $('.chat_input').val('');
            $('.msg_container_base').append(data);

            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
            get_message()
        })
        .fail(function (data) {
            console.log(data)
        });
    return false;
});

function get_message() {
    $.ajax({
        url: "/messages/get/",
        type: "GET",
        async: false
    })
        .done(function (data) {
            $('.msg_container_base').append(data);
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
            if (data) {
                read_message();
            }
        })
        .fail(function (data) {
            console.log('not receive');
        })
        .always(
            setTimeout(get_message, 5000)
        );
}

function read_message() {
    $.ajax({
        url: "/messages/read/",
        type: "POST",
        async: false
    })
}

