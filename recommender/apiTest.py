import requests
from requests.auth import HTTPBasicAuth
import os
from django.conf import settings
import json
import time
from operator import attrgetter
from Game import Game

# TODO
"""
+ Produce list of ongoing Games from json Scoreboard response
    + Create skeleton python object for a game
    + Extract individual games from json Scoreboard response
    + Write constructor for python Game object that takes in a json game object

+ Create pretty print method for Game

+ Sort Game list into proper priority
    + Create basic weighting for Game object
    + Weight based only on time remaining
    + Figure out how to sort objects in python

x Produce and sort list with every response
    x Test execution time of algorithm so far (less than 1 minute essential)
    x Pull from local data every minute, run algorithm, pretty print results
    ^ Optimize as necessary

+ <Optional> Use Materialize to improve look and feel

x Get working as web app
    x Make server get json from local file every minute and run getGameList
        x hardcode list of games in demo.html
        x get list of games once from log.txt and display
        x display each game as separate html element
        x request from local file repeatedly
        x request next sb object from local file each time
    x Request particular game from local gameList with localOne
    x Make input for seconds to wait between requests
    x Poll from NFL Scoreboard feed every minute and run getGameList
    x Make game display look nice

- Improve Weighting algorithm
    Note: may be better to create multiple versions of getPriority (e.g. getPriority0(), getPriority1())
    x time remaining
    x score
    x yard line
        <optional> consider whether trailing team has possession
    - team records
        <optional> weight games within division higher
    - General Tuning (see getPriority() method in Game.py)

- Implement basic user profiles ***Tuesday 11/29***
    - Create register and login pages (no authentication yet)
    - Direct to demo
        - Include submit button and demo button
    - Store username and password in database
    - Display username at top of screen
    <optional> Ask for and save favorite teams

- Personalize weights based on user input ***Tuesday 11/29 - Thursday 11/30***
    - Use fafreco23vorite teams in weighting
    - Make up/down buttons next to each game's display
    - Make upvote add flat number to weight for some amount of time
    - Evaluate and make  adjustments

- Make "actual" web app ***Thursday 12/01 - Friday 12/02***
    - Requests scoreboard every minute on load
    - Display details if no scoreboard
        - display simple "check back sunday" message
        - display games on Sunday ranked by gametime
        - display games on Sunday also ranked by team record

<optional> Potential improvements to feedback feature ***Friday 12/02***
    - Ask user basic questions on why game is in wrong spot (e.g. score not close enough, too much time, don't like teams)
    - Adjust weighting based on response

- Testing and adjusting ***Sunday 11/27 and Sunday 12/04***
    - Use app throughout NFL Sunday
    - Address problems as necessary

***Note***
    - Minimum Viable Product acheived at this point
    - Everything after is gravy
    - Sanding rough edges most important, then fine tuning to look more impressive

- General bug fixing ***Sunday 11/27 - Sunday 11/04***
    - Fix any remaining persistent bugs
    - Improve aspects that feel shoddy, but may not necessarily be bugs

- *Optional* Fine tuning
    - Continue to tune default weighting
    ^ Continue to tune feedback mechanism
    - Improve UI

- Prepare deliverables ***Sunday 11/27 - Sunday 12/04***
"""

"""
gamestate = sbd["scoreboard"]["gameScore"][0]
down = gamestate["currentDown"]
distance = gamestate["currentYardsRemaining"]
yardline = gamestate["lineOfScrimmage"] # dict
"""

# TODO Prompt for username and password at startup
USERNAME = "devinjohnston17"
PASSWORD = ""

CURRENT_SEASON = "2016-2017-regular"

def getFullSchedule():
    url_schedule = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + \
            "/full_game_schedule.json"
    r = requests.get(url_schedule, auth=(USERNAME, PASSWORD))
    return r.text

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

def getNowString():
    fordate = '20161106'
    #sb = getScoreboard(fordate)
    sb = getScoreboard(fordate, True)
    d = json.loads(sb)
    gl = getGameList(d)

    returnStr = ''
    for game in gl:
        returnStr += game.__str__() + '\n\n'

    return returnStr


# TODO Catch Ctrl-c
# TODO Encapsulate responses in json object
def logResponses(n):
    log = open("11_06.txt", "w")
    fordate = "20161106"
    log.write('[')
    for i in range(n):
        log.write(getScoreboard(fordate))
        if i != n - 1:
            log.write(",")
        time.sleep(60)
    log.write(']')
    log.close()

def main():
    f = open('log.txt', 'r')
    text = f.read()
    f.close()

    getGameList(text)

if __name__ == "__main__":
    main()
