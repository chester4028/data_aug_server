
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/sentence');
    var sentences_received = [];

    //receive details from server
    socket.on('newsentence', function(msg) {
        console.log("Received sentence" + msg.sentence);
        if (sentences_received.length >= 100){
            sentences_received.shift();
        }
        if (sentences_received.includes(msg.sentence)) {
          return;
        }
        sentences_received.push(msg.sentence);
        sentences_string = '';
        for (var i = 0; i < sentences_received.length; i++){
            sentences_string = sentences_string + '<p>' + sentences_received[i].toString() + '</p>';
        }
        $('#sentences').html(sentences_string);
    });

    $('form#sentence_form').submit(function (event) {
        console.log('send sentence');
        sentences_received = [];
        $('#sentences').html('');
        sentences_string = $('#sentences_string').val();
        if (sentences_string == undefined || sentences_string === "") {
            return false;
        }
        socket.emit('gen_sentence', {sentence: sentences_string});
        return false;
    });

    $(window).on("beforeunload", function(e) {
        socket.emit('close_job');
        console.log("bye bye");
    });
});
