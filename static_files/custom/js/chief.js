var dnperm = document.getElementById('dnperm');
var dntrigger = document.getElementById('dntrigger');


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

dnperm.addEventListener('click', function (e) {
    e.preventDefault();
    if (!window.Notification) {
        alert('Sorry, notifications is not supported.');
    } else {
        Notification.requestPermission(function (permission) {
            if (permission === 'denied') {
                alert('You have denied notifications')
            } else (permission === 'granted')
            {
                alert('You have granted notifications')
            }
        })
    }
});

function get_first_message() {
    $.ajax({
        url: "/messages/seen/",
        type: "GET"
    })
        .done(function (data) {
            $('.new_mess').append(data);
            if (data) {
                var notify;
                notify = new Notification('+', {
                    body: 'Новый диалог',
                    icon: 'data:image/png;base64,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',
                });
            }
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
                var notify;
                notify = new Notification('+', {
                    body: 'Новое сообщение',
                    icon: 'data:image/png;base64,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',
                });
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

