var socket = new WebSocket("ws://" + window.location.host + "/recommender/demo/");
var gameList = []

socket.onmessage = function(message) {
    //alert(message.data);
    dataObject = JSON.parse(message.data);
    gameList = dataObject.games;
    displayGameList();
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

function displayGameList() {
    $('#games').empty();
    for (var i = 0; i < gameList.length; i++) {
        var game = gameList[i];
        $('#games').append('<p>' + toString(game) + '</p>');
        if (i != gameList.length - 1) $('#games').append('<button id="toohigh' + i + '" class="btn waves-effect waves-light">Too High</button>');
        if (i != 0) $('#games').append('<button id="toolow' + i + '" class="btn waves-effect waves-light">Too Low</button>');
    }
}

function toString(game) {
    s = "";
    s += "Ranking Score: " + game.priority + "\n";
    s += game.rankscore + "\n";
    s += "------------\n";
    s += game.homeTeam + ": " + game.homeScore + "\n";
    s += game.awayTeam + ": " + game.awayScore + "\n";
    if (game.isPrestart) {
        s += "Starting Soon...";
    }
    else if (game.isHalftime) {
        s += "Halftime";
    }
    else {
        s += "Quarter: " + game.quarter + "   Remaining: " +
                Math.floor(game.timeRemaining / 60) + ":" + zeroPad(game.timeRemaining % 60) + "\n";
        if (game.possession) {
            s += "Possession: " + game.possession + "\n";
            s += game.down + " and " + game.toGo + " on the " + game.yardLine.team +
                    " " + game.yardLine.yardLine;
        }
        else {
            s += "API Error?"
        }
    }
    return s
}

function zeroPad(num) {
    num = num + ""
    return num.length > 1 ? num : "0" + num
}
