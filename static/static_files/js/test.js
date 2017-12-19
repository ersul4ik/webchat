$( document ).ready(function() {
$('body').append('<div id="form-chat"></div>');
$.ajax('http://127.0.0.1:8000/chat/').done(function(data){$('#form-chat').html(data)});
console.log('replay');
});