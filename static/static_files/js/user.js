$('#chat-form').on('submit', function(event){
    event.preventDefault();
    $.ajax({
        url : '/chat/',
        type : 'POST',
        data : $( this ).serialize(),
        success : function(data){
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

function Sent_Get() {
	  $.ajax({
          url: "/chat/",
          type: "GET",
          dataType: "json",
          data: $( this ).serialize(),
          success: function (data) {
              $('.chat_input').val('');
              $('.msg_container_base').append(data);
              console.log('ok');

              var chatlist = document.getElementById('msg-list-div');
              chatlist.scrollTop = chatlist.scrollHeight;
          }
      })};
