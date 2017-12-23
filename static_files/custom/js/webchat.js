/**
 * Тут минимум js кода
 */

var ChatNode = $('<div class="webchat" id="webchat"></div>');

$(document).ready(function () {
        $('body').append(ChatNode);
        LoadWebChat(ChatNode);
        if ($('.name-input').length === 0) {
            get_message(ChatNode)
        }
    }
);

// Загружает чат и вставляет в нужный элемент
function LoadWebChat(node) {
    var url = $('#webchatJS').data('url') + 'chat/';
    $.ajax(url, {
        method: 'GET',
        async: false,
        crossDomain: true,
        xhrFields: {withCredentials: true}
    })
        .done(function (data) {
            node.append(data)
        })
        .fail(function () {
            console.log('Can`t load chat form!')
        });
}

// Это копипист ТРЕБУЮЩИЙ рефактора!!!!!
$(document).on('submit', '#chat-form', function(e) {
    CreateDialog($( this ));
    return false;
});

function CreateDialog(node) {
    var url = $('#webchatJS').data('url') + 'chat/?create';
    $.ajax({
        url: url,
        async: false,
        type: node.attr('method'),
        data: node.serialize(),
        crossDomain: true,
        xhrFields: {withCredentials: true}
    })
        .done(function (data) {
            $('.name-input').remove();
            $('.chat_input').val('');
            $('.msg_container_base').append(data);

            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;

            get_message(node)
        })
        .fail(function (data) {
            console.log('ajax method fail')
        });
}

function get_message(node) {
    var url = $('#webchatJS').data('url') + 'messages/get/';
    $.ajax({
        url: url,
        async: false,
        crossDomain: true,
        xhrFields: {withCredentials: true}
    })
        .done(function (data) {
            // Это не хорошо. Нужно искать элемент в node
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
    var url = $('#webchatJS').data('url') + 'messages/read/';
    $.ajax({
        url: url,
        type: "POST",
        async: false,
        crossDomain: true,
        xhrFields: {withCredentials: true}
    })
}

$(document).ready(function() {
    $("#chat_window_1").fadeIn(500); // плавное появление блока "чата"
    var $this = $('#minim_chat_window');
    $this.parents('.panel').find('.panel-body').slideUp();
    $this.parents('.panel').find('.panel-footer').slideUp();
    $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
    $this.addClass('panel-collapsed');

});
$(document).on('click', '.panel-heading h3.chat-open', function (e) {
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.parents('.panel').find('.panel-footer').slideUp();
        // $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
        $this.addClass('panel-collapsed');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.parents('.panel').find('.panel-footer').slideDown();
        $this.removeClass('panel-collapsed');
        // $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('click', '.panel-heading span.icon_minim', function (e) {
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.parents('.panel').find('.panel-footer').slideUp();
        $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
        $this.addClass('panel-collapsed');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.parents('.panel').find('.panel-footer').slideDown();
        $this.removeClass('panel-collapsed');
        $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('focus', '.panel-footer input.chat_input', function (e) {
    var $this = $(this);
    if ($('#minim_chat_window').hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.parents('.panel').find('.panel-footer').slideDown();
        $('#minim_chat_window').removeClass('panel-collapsed');
        $('#minim_chat_window').removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('click', '#new_chat', function (e) {
    var size = $( ".chat-window:last-child" ).css("margin-left");
     size_total = parseInt(size) + 400;
    alert(size_total);
    var clone = $( "#chat_window_1" ).clone().appendTo( ".container" );
    clone.css("margin-left", size_total);
});
$(document).on('click', '.icon_close', function (e) {
    //$(this).parent().parent().parent().parent().remove();
    $( "#chat_window_1" ).remove();
});
