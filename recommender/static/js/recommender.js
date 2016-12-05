// Used for sending messages and requests back and forth to the server
var socket = new WebSocket("ws://" + window.location.host + "/recommender/demo/");
var gameList = []

// Displays game data on receipt of a response from the server
socket.onmessage = function(message) {
    //alert(message.data);
    dataObject = JSON.parse(message.data);
    gameList = dataObject.games;
    displayGameList();
}

// Gets a single list of games from a local file
$('#localPollOne').on('click', function(event) {
    username = $('#username').text()
    var message = username + " localOne " + $('#index').val();
    socket.send(message);
    return false;
});


// Repeatedly gets consecutive lists of games from a local file
$('#localPollRepeat').on('click', function(event) {
    username = $('#username').text()
    var message = username + " localRepeat " + $('#wait').val();
    socket.send(message);
    return false;
});

// Gets a single list of live games 
$('#livePollOne').on('click', function(event) {
    username = $('#username').text();
    var message = username + " liveOne";
    socket.send(message);
    return false;
});

// Repeatedly gets lists of live games. For demo only.
$('#livePollRepeat').on('click', function(event) {
    username = $('#username').text();
    var message = username + " liveRepeat " + $('#wait').val();
    socket.send(message);
    return false;
});

// For debugging and demoing. Resets weights to defaults.
$('#resetWeights').on('click', function(event) {
    username = $('#username').text();
    var message = username + " resetWeights";
    socket.send(message)
    return false;
});

// Repeatedly gets lists of live games. For main application.
$('#main').on('click', function(event) {
    username = $('#username').text();
    var message = username + " liveRepeat 60"
    socket.send(message);
    return false;
});

// Displays string representations of games and produces corresponding appropriate toohigh/toolow buttons
function displayGameList() {
    $('#games').empty();
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

// Converts json Game object into a nice-looking string representation for display on page
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

// For formatting seconds in time remaining
function zeroPad(num) {
    num = num + ""
    return num.length > 1 ? num : "0" + num
}

/*
 * Called when "Too High" is pressed.
 * Determines metric whose weight should be reduced.
 * Finds metric for selected game whose value is the highest above
 * the value for the game immediately below in ranking. Then sends
 * message to server telling it to reduce the weight for that metric.
 */
function reducePlacement(gameIndex) {
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
    var message = username + " reduce " + toReduce
    socket.send(message)
    alert('Got it!')
}

/*
 * Called when "Too Low" is pressed.
 * Determines metric whose weight should be increased.
 * Finds metric for selected game whose value is the highest above
 * the value for the game immediately above in ranking. Then sends
 * message to server telling it to increase the weight for that metric.
 */
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
    var message = username + " increase " + toIncrease
    socket.send(message)
    alert('Got it!')
}
