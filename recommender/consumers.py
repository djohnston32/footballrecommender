import json
import time
import requests
from requests.auth import HTTPBasicAuth
import os
from django.conf import settings
from operator import attrgetter
from Game import Game


# Data access functions

# TODO Prompt for username and password at startup
USERNAME = "devinjohnston17"
PASSWORD = ""

CURRENT_SEASON = "2016-2017-regular"

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

# decoded = json.loads(requestText)
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

def getNowString(useLocal=False):
    # TODO Get today's date
    fordate = '20161127'
    sb = getScoreboard(fordate, useLocal)
    d = json.loads(sb)
    nowString = getGameString(d)

    return nowString

def getSbList():
    log = open(os.path.join(settings.BASE_DIR, '11_06.txt'))
    sbString = log.read()
    log.close()

    sbList = json.loads(sbString)
    return sbList


# Respond to message
def ws_message(message):
    print type(message)
    if "localOne" in message.content['text']:
        sbList = getSbList()
        i = int(message.content['text'].split()[1])
        gameString = getGameString(sbList[i])
        message.reply_channel.send({
            "text": gameString
        })

    elif "localRepeat" in message.content['text']:
        seconds = int(message.content['text'].split()[1])
        sbList = getSbList()
        for i in range(len(sbList)):
            gameString = getGameString(sbList[i])
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
