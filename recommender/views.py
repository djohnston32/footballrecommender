from django.shortcuts import render
from django.http import HttpResponse

import requests
from requests.auth import HTTPBasicAuth

import os
from django.conf import settings

import json
import time
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
def getGameList(decoded):
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
    return sorted(gameList, key=attrgetter('priority'), reverse=True)

def getNowList():
    fordate = '20161106'
    #sb = getScoreboard(fordate)
    sb = getScoreboard(fordate, True)
    d = json.loads(sb)
    gl = getGameList(d)

    nowList = []
    for game in gl:
        nowList.append(game.__str__())

    return nowList


# Views

def index(request):
    return render(request, "index.html")

def demo(request):
    context = {
        'nowList': getNowList()
    }
    return render(request, "demo.html", context)
