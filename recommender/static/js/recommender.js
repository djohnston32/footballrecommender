var socket = new WebSocket("ws://" + window.location.host + "/recommender/demo/");
var gameList = []

socket.onmessage = function(message) {
    //alert(message.data);
    dataObject = JSON.parse(message.data);
    gameList = dataObject.games;
    displayGameList();
}

$('#localPollOne').on('click', function(event) {
    username = $('#username').text()
    var message = username + " localOne " + $('#index').val();
    socket.send(message);
    return false;
});


$('#localPollRepeat').on('click', function(event) {
    username = $('#username').text()
    var message = username + " localRepeat " + $('#wait').val();
    socket.send(message);
    return false;
});

$('#livePollOne').on('click', function(event) {
    username = $('#username').text();
    var message = username + " liveOne";
    socket.send(message);
    return false;
});

$('#livePollRepeat').on('click', function(event) {
    username = $('#username').text();
    var message = username + " liveRepeat " + $('#wait').val();
    socket.send(message);
    return false;
});

$('#resetWeights').on('click', function(event) {
    username = $('#username').text();
    var message = username + " resetWeights";
    socket.send(message)
    return false;
});

$('#main').on('click', function(event) {
    username = $('#username').text();
    var message = username + " liveRepeat 10"
    socket.send(message);
    return false;
});

function displayGameList() {
    $('#games').empty();
    console.log("Entering displayGameList()")
    if (gameList.length == 0) {
        $('#games').append('<p>No games are being played right now. Check back later!</p>');
    } else {
        for (var i = 0; i < gameList.length; i++) {
            var game = gameList[i];
            $('#games').append('<p>' + toString(game) + '</p>');
            if (i != gameList.length - 1) {
                $('#games').append('<button id="toohigh' + i +
                    '" class="btn waves-effect waves-light">Too High</button>');
                $('#toohigh' + i).on('click', function(event) {
                    var gameIndex = parseInt((event.target.id).replace(/[^0-9\.]/g, ''));
                    reducePlacement(gameIndex);
                });
            }
            if (i != 0) {
                $('#games').append('<button id="toolow' + i +
                    '" class="btn waves-effect waves-light">Too Low</button>');
                $('#toolow' + i).on('click', function(event) {
                    var gameIndex = parseInt((event.target.id).replace(/[^0-9\.]/g, ''));
                    increasePlacement(gameIndex);
                });
            }
        }
    }
}

function toString(game) {
    s = "";

    var path = window.location.pathname;
    if (path == "/recommender/demo/") {
        s += "Ranking Score: " + game.priority + "\n";
        s += game.rankscore + "\n";
        s += "------------\n";
    }

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

function reducePlacement(gameIndex) {
    console.log("Entering reducePlacement()")
    console.log(gameList.length)
    console.log(gameIndex)
    var metrics = ['pScore', 'pTime', 'pYardLine', 'pRank']
    var greatestDiff = -1;
    var toReduce = '';
    for (var i = 0; i < metrics.length; i++) {
        diff = gameList[gameIndex][metrics[i]] - gameList[gameIndex+1][metrics[i]];
        if (diff > greatestDiff) {
            greatestDiff = diff;
            toReduce = metrics[i]
        }
    }
    username = $('#username').text()
    console.log(username)
    var message = username + " reduce " + toReduce
    socket.send(message)
    alert('Got it!')
}

function increasePlacement(gameIndex) {
    var metrics = ['pScore', 'pTime', 'pYardLine', 'pRank']
    var greatestDiff = Number.NEGATIVE_INFINITY;
    var toIncrease= '';
    for (var i = 0; i < metrics.length; i++) {
        diff = gameList[gameIndex][metrics[i]] - gameList[gameIndex-1][metrics[i]];
        if (diff > greatestDiff) {
            greatestDiff = diff;
            toIncrease = metrics[i]
        }
    }
     
    username = $('#username').text()
    console.log(username)
    var message = username + " increase " + toIncrease
    socket.send(message)
    alert('Got it!')
}
