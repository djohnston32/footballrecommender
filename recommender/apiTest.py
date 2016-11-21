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
    + Figure out how to sort shit in python (python equivalent of java comparator method?)

- Get working as web app with local data
    - Make server get json from local file every minute and run getGameList
        x hardcode list of games in demo.html
        x get list of games once from log.txt and display
        x display each game as separate html element
        - request from local file repeatedly
        - request next sb object from local file each time
            - Make log file with multiple scoreboard objects iterable
    - Make game display look nice
    + Make frontend look nice using Materialize

^ Improve Weighting algorithm
    Note: may be better to create multiple versions of getPriority (e.g. getPriority0(), getPriority1())
    - time remaining
    - score
    - yard line (eventually consider whether trailing team has possession)
    - team records (eventually weight games within division higher)

x Produce and sort list with every response
    x Test execution time of algorithm so far (less than 1 minute essential)
    x Pull from local data every minute, run algorithm, pretty print results
    ^ Optimize as necessary

- Get web app working on real time data
    ^ Write startup and exit functions to cleanly begin and end polling
    - Poll from NFL Scoreboard feed every minute and run getGameList
    ^ Where possible, optimize algorithm to only update objects when necessary

*** Sunday 11/13 at 11:55 PM

+ *Optional* Use Materialize to improve look and feel

- Implement basic user profiles
    - Create register and login pages (no authentication yet)
    - Store username and password in database
    - Display username at top of screen
    ^ Ask for and save favorite teams?

- Personalize weights based on user input
    ^ Use favorite teams in weighting
    - Make up/down buttons next to each game's display
    - Make upvote add flat number to weight for some amount of time
    ^ Evaluate and make  adjustments

- Potential improvements to feedback feature
    ^ Ask user basic questions on why game is in wrong spot (e.g. score not close enough, too much time, don't like teams)
    - Adjust weighting based on response

*** Saturday 11/19 at 11:55 PM

- Testing and adjusting
    - Use app throughout NFL Sunday
    - Address problems as necessary

*** Sunday 11/20 at 11:55 PM

***Note***
    - Minimum Viable Product acheived at this point
    - Everything after is gravy
    - Sanding rough edges most important, then fine tuning to look more impressive

- General bug fixing - Week of 11/14
    - Fix any remaining persistent bugs
    - Improve aspects that feel shoddy, but may not necessarily be bugs

- *Optional* Fine tuning: 11/21 - 11/30
    - Continue to tune default weighting
    ^ Continue to tune feedback mechanism
    - Improve UI

- Prepare deliverables: 12/01 - 12/06
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
