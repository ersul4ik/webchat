$( document ).ready(function() {
$.ajax('http://127.0.0.1:8000/chat/').done(function(data){$('#form-chat').html(data)});
});