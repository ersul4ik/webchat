$(document).ready(function () {
    if ($('#chat-form')) {
        get_message()
    }
    else{
        get_message_seen()
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

function get_message_seen() {
    $.ajax({
        url: "/messages/get/",
        type: "GET",
        async: false
    })
        .done(function (data) {
            $('#message-receive').append(data);
            if (data) {
                read_message();
            }
        })
        .fail(function (data) {
            console.log('error receive');
        })
        .always(
            setTimeout(get_message, 8000)
        );
}

function get_message() {
    $.ajax({
        url: "/messages/get/",
        type: "GET",
        async: false
    })
        .done(function (data) {
            $('#message-receive').append(data);
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
            setTimeout(get_message, 8000)
        );
}

function read_message() {
    $.ajax({
        url: "/messages/read/",
        type: "POST",
        async: false
    })
}


//
// function get_message_list() {
//     $.ajax({
//         url: "/messages/list/",
//         type: "GET",
//         async: false
//     })
//         .done(function (data) {
//             $('.not-view').append(data);
//             if(data){
//                 seen_message();
//             }
//             console.log('ok')
//         })
//         .fail(function (data) {
//             console.log('Message not receive');
//         })
//         .always(
//             setTimeout(get_message_list, 6000)
//         );
// }


// function seen_message() {
//     $.ajax({
//         url: "/messages/seen/",
//         type: "POST",
//         async: false
//     })
// }
