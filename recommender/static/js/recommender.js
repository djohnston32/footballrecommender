var socket = new WebSocket("ws://" + window.location.host + "/recommender/demo/");

socket.onmessage = function(message) {
    //alert(message.data);
    $('#games').empty()
    $('#games').append('<p>' + message.data + '</p>')
}

$('#localPollOne').on('click', function(event) {
    var message = "localOne " + $('#index').val();
    socket.send(message);
    return false;
});


$('#localPollRepeat').on('click', function(event) {
    var message = "localRepeat " + $('#wait').val();
    socket.send(message);
    return false;
});

$('#livePollOne').on('click', function(event) {
    var message = "liveOne";
    socket.send(message);
    return false;
});

$('#LivePollRepeat').on('click', function(event) {
    var message = "liveRepeat " + $('#wait').val();
    socket.send(message);
    return false;
});
