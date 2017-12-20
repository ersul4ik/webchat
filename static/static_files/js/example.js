$('#chat-form').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        url: 'http://127.0.0.1:8000/chat/',
        type: "POST",
        data: $(this).serialize(),
        crossDomain: false
    })
        .done(function (data) {
            $('.name-input').remove();
            $('.chat_input').val('');
            $('.msg_container_base').append(data);

            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        })
        .fail(function (data) {
            console.log('ajax method fail')
        });
    return false;
});
