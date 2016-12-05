import json
import time
import requests
from requests.auth import HTTPBasicAuth
import os
from django.conf import settings
from operator import attrgetter
from Game import Game
from channels import Group
from django.contrib.auth.models import User


# Data access functions

USERNAME = "devinjohnston17"
PASSWORD = "freco23"

CURRENT_SEASON = "2016-2017-regular"

# Get team rankings from MySportsFeeds API
def getStandings():
    url_standings = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + \
            "/overall_team_standings.json?teamstats=W"
    r = requests.get(url_standings, auth=(USERNAME, PASSWORD))
    standings = json.loads(r.text)
    teamList = standings['overallteamstandings']['teamstandingsentry']
    rankings = {}
    for team in teamList:
        rankings[team['team']['Abbreviation']] = team['rank']
    return rankings

"""
    In the MySportsFeeds API, a scoreboard is a snapshot providing current data
    for all games on a particular day. This function is called every time the
    application needs to update using live data.
"""
def getScoreboard(fordate, useLocal=False):
    if useLocal:
        log = open(os.path.join(settings.BASE_DIR, 'log.txt'))
        text = log.read()
        log.close()
    else:
        url_scoreboard = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + \
                "/scoreboard.json?fordate=" + fordate
        text = requests.get(url_scoreboard, auth=(USERNAME, PASSWORD)).text
    return text

# Old method here for reference. Using getJsonString() now instead.
def getGameString(decoded):
    gameList = []
    for gameDict in decoded["scoreboard"]["gameScore"]:
        if str(gameDict["isInProgress"]) == "true":
            try:
                game = Game(gameDict)
                #print game
                gameList.append(game)
            except KeyError as err:
                print "Error"
                print err
                print gameDict

    gl = sorted(gameList, key=attrgetter('priority'), reverse=True)
    gameString = ""
    for game in gl:
        gameString += game.__str__() + "\n\n"

    return gameString

"""
    Turns a scoreboard response from MySportsFeeds into a list of Game objects,
    and then turns those Game objects into a JSON string containing a list of
    simple JSON representations of the Game objects. This string is what gets sent
    to the client when it requests game data.
"""
def getJsonString(decoded, weights):
    gameList = []
    for gameDict in decoded["scoreboard"]["gameScore"]:
        if str(gameDict["isInProgress"]) == "true":
            try:
                game = Game(gameDict, weights)
                #print game
                gameList.append(game)
            except KeyError as err:
                print "Error"
                print err
                print gameDict

    gl = sorted(gameList, key=attrgetter('priority'), reverse=True)
    jsonString = "{\"games\":["
    for game in gl:
        jsonString += game.toJsonString()
        jsonString += ","
    if jsonString[-1] == ",":
        jsonString = jsonString[:-1]
    jsonString += "]}"

    return jsonString

# Gets live data and performs getJsonString() on it
def getNowString(weights, useLocal=False):
    # TODO Get today's date
    fordate = '20161204'
    sb = getScoreboard(fordate, useLocal)
    d = json.loads(sb)
    nowString = getJsonString(d, weights)

    return nowString

# For debugging and demoing. Gets a list of scoreboards from a local file.
def getSbList():
    log = open(os.path.join(settings.BASE_DIR, '11_06.txt'))
    sbString = log.read()
    log.close()

    sbList = json.loads(sbString)
    return sbList


# Channels code

# Add to main group on websocket.connect
def ws_add(message):
    Group("main").add(message.reply_channel)

# Respond to message from client
def ws_message(message):

    # Reduce weight of a certain metric. Called when a "Too High" button is clicked
    if "reduce" in message.content['text']:
        username = message.content['text'].split()[0]
        toReduce = message.content['text'].split()[2]
        print "Reducing: " + toReduce
        user = User.objects.get(username=username)
        if toReduce == "pScore" and user.profile.pScore > 1:
            user.profile.pScore -= 1
        elif toReduce == "pTime" and user.profile.pTime > 1:
            user.profile.pTime -= 1
        elif toReduce == "pYardLine" and user.profile.pYardLine > 1:
            user.profile.pYardLine -= 1
        elif toReduce == "pRank" and user.profile.pRank > 1:
            user.profile.pRank -= 1

        user.save()

        print user.profile.pScore
        print user.profile.pTime
        print user.profile.pYardLine
        print user.profile.pRank

    # Increase weight of a certain metric. Called when a "Too Low" button is clicked
    elif "increase" in message.content['text']:
        username = message.content['text'].split()[0]
        toIncrease = message.content['text'].split()[2]
        print "Increasing: " + toIncrease
        user = User.objects.get(username=username)
        user.profile.pScore += 1
        if toIncrease == "pScore":
            user.profile.pScore += 1
        elif toIncrease == "pTime":
            user.profile.pTime += 1
        elif toIncrease == "pYardLine":
            user.profile.pYardLine += 1
        elif toIncrease == "pRank":
            user.profile.pRank += 1

        user.save()

        print user.profile.pScore
        print user.profile.pTime
        print user.profile.pYardLine
        print user.profile.pRank

    # Resets the weights to their defaults.
    elif "resetWeights" in message.content['text']:
        username = message.content['text'].split()[0]
        user = User.objects.get(username=username)
        print "Resetting weights"
        user.profile.pScore = 10
        user.profile.pTime = 10
        user.profile.pYardLine = 5
        user.profile.pRank = 5
        user.save()

        print user.profile.pScore
        print user.profile.pTime
        print user.profile.pYardLine
        print user.profile.pRank

    # Responds with a single ranked list of games from a local file
    elif "localOne" in message.content['text']:
        sbList = getSbList()
        username = message.content['text'].split()[0]
        i = int(message.content['text'].split()[2])

        user = User.objects.get(username=username)
        weights = [user.profile.pScore, user.profile.pTime, \
                user.profile.pYardLine, user.profile.pRank]
        gameString = getJsonString(sbList[i], weights)

        message.reply_channel.send({
            "text": gameString
        })

    # Responds repeatedly with consecutive ranked game lists from a local file
    elif "localRepeat" in message.content['text']:
        username = message.content['text'].split()[0]
        seconds = int(message.content['text'].split()[2])
        sbList = getSbList()
        for i in range(len(sbList)):
            user = User.objects.get(username=username)
            weights = [user.profile.pScore, user.profile.pTime, \
                user.profile.pYardLine, user.profile.pRank]
            gameString = getJsonString(sbList[i], weights)

            message.reply_channel.send({
                "text": gameString
            })
            time.sleep(seconds)

    # Responds with a single ranked list of live games
    elif "liveOne" in message.content['text']:
        username = message.content['text'].split()[0]

        user = User.objects.get(username=username)
        weights = [user.profile.pScore, user.profile.pTime, \
                user.profile.pYardLine, user.profile.pRank]

        message.reply_channel.send({
            "text": getNowString(weights)
        })

    # Primary feature of the application. Responds repeatedly with ranked lists of live games.
    # This is called when "Start Recommending" is pressed on the main page
    elif "liveRepeat" in message.content['text']:
        username = message.content['text'].split()[0]
        seconds = int(message.content['text'].split()[2])
        while True:
            user = User.objects.get(username=username)
            weights = [user.profile.pScore, user.profile.pTime, \
                    user.profile.pYardLine, user.profile.pRank]

            message.reply_channel.send({
                "text": getNowString(weights)
            })
            time.sleep(seconds)

    # Request not recognized
    else:
        message.reply_channel.send({
            "text": "ERROR: action not received or not recognized",
        })

# Remove from main group on websocket.disconnect
def ws_disconnect(message):
    Group("main").discard(message.reply_channel)
