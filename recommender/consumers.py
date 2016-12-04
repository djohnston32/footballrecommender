import json
import time
import requests
from requests.auth import HTTPBasicAuth
import os
from django.conf import settings
from operator import attrgetter
from Game import Game
from channels import Group


# Data access functions

# TODO Prompt for username and password at startup
USERNAME = "devinjohnston17"
PASSWORD = ""

CURRENT_SEASON = "2016-2017-regular"

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
                print err
                print gameDict
            #print "\n"

    gl = sorted(gameList, key=attrgetter('priority'), reverse=True)
    gameString = ""
    for game in gl:
        gameString += game.__str__() + "\n\n"

    return gameString

def getJsonString(decoded):
    gameList = []
    for gameDict in decoded["scoreboard"]["gameScore"]:
        if str(gameDict["isInProgress"]) == "true":
            try:
                game = Game(gameDict)
                #print game
                gameList.append(game)
            except KeyError as err:
                print err
                print gameDict
            #print "\n"

    gl = sorted(gameList, key=attrgetter('priority'), reverse=True)
    jsonString = "{\"games\":["
    for game in gl:
        jsonString += game.toJsonString()
        jsonString += ","
    if jsonString[-1] == ",":
        jsonString = jsonString[:-1]
    jsonString += "]}"

    return jsonString

def getNowString(useLocal=False):
    # TODO Get today's date
    fordate = '20161127'
    sb = getScoreboard(fordate, useLocal)
    d = json.loads(sb)
    nowString = getJsonString(d)

    return nowString

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

# Respond to message
def ws_message(message):
    if "main" in message.content['text']:
        Group("main").send({
            "text": "TODO"
        })

    elif "localOne" in message.content['text']:
        sbList = getSbList()
        i = int(message.content['text'].split()[1])
        gameString = getJsonString(sbList[i])
        message.reply_channel.send({
            "text": gameString
        })

    elif "localRepeat" in message.content['text']:
        seconds = int(message.content['text'].split()[1])
        sbList = getSbList()
        for i in range(len(sbList)):
            gameString = getJsonString(sbList[i])
            message.reply_channel.send({
                "text": gameString
            })
            time.sleep(seconds)

    elif message.content['text'] == "liveOne":
        message.reply_channel.send({
            "text": getNowString()
        })

    elif "liveRepeat" in message.content['text']:
        seconds = int(message.content['text'].split()[1])
        while True:
            message.reply_channel.send({
                "text": getNowString()
            })
            time.sleep(seconds)

    else:
        message.reply_channel.send({
            "text": "Action not received or not recognized",
        })

# Remove from main group on websocket.disconnect
def ws_disconnect(message):
    Group("main").discard(message.reply_channel)
