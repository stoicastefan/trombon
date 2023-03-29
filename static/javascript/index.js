$(document).ready(function() {
    namespace = '/test';
    var socket = io(namespace);

    socket.on('connect', function() {
        socket.emit('my_event', {data: 'connected to the SocketServer...'});
        console.log("coooooonnnneeeecccttt")
    });

    socket.on('my_response', function(msg, cb) {
        $('#log').append('<br>' + $('<div/>').text('logs #' + msg.count + ': ' + msg.data + ' || ' + msg.number_of_cards.r11).html());
        if (cb)
            cb();
    });
    $('form#username').submit(function(event) {
        socket.emit('join', {username: $('#username_data').val(), room: $('#room_data').val()});
        return false;
    });
    $('form#emit').submit(function(event) {
        socket.emit('my_event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        console.log(event)
        console.log($('#broadcast_data').val())
        socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
        return false;
    });
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect_request');
        return false;
    });
});