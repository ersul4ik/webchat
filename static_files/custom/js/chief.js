$(document).ready(function () {
    if ($('#receive_mess').length == 0) {
        get_first_message();
    }
    else {
        get_message()
    }
    if ($('#dialogs').length == 1) {

        get_following_messages()
    }
    else {
    }
});

$('#chat-form').on('submit', function (event) {
    event.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: $(this).serialize()
    })
        .done(
            function (data) {
                $('.name-input').remove();
                $('.chat_input').val('');
                $('.msg_container_base').append(data);

                var chatlist = document.getElementById('msg-list-div');
                chatlist.scrollTop = chatlist.scrollHeight;
                get_message()
            });
    return false
});

function get_first_message() {
    $.ajax({
        url: "/messages/seen/",
        type: "GET"
    })
        .done(function (data) {
            $('.new_mess').append(data);

        })
        .fail(function (data) {
            console.log('error receive');
        })
        .always(
            setTimeout(get_first_message, 7000)
        );
}

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
            console.log('error receive');
        })
        .always(
            setTimeout(get_message, 6000)
        );
}

function get_following_messages() {
    $.ajax({
        url: "/messages/receive/",
        type: "GET"
    })
        .done(function (data) {
            $('.new_mess').append(data);

        })
        .fail(function (data) {
            console.log('error receive');
        })
        .always(
            setTimeout(get_following_messages, 6000)
        );
}

function read_message() {
    $.ajax({
        url: "/messages/read/",
        type: "POST",
        async: false,
        crossDomain: true,
        xhrFields: {withCredentials: true}
    })
}

