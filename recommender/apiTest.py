import requests
from requests.auth import HTTPBasicAuth
import json
import time

# TODO
"""
gamestate = sbd["scoreboard"]["gameScore"][0]
down = gamestate["currentDown"]
distance = gamestate["currentYardsRemaining"]
yardline = gamestate["lineOfScrimmage"] # dict

- Produce list of ongoing Games from json Scoreboard response
    - Create skeleton python object for a game
    - Extract individual games from json Scoreboard response
    ^ Write constructor for python Game object that takes in a json game object

- Create pretty print method for Game

- Sort Game list into proper priority
    - Create basic weighting for Game object
    - Weight based only on time remaining
    ^ Figure out how to sort shit in python (python equivalent of java comparator method?)

^ Improve Weighting algorithm
    - time remaining
    - score
    - yard line (eventually consider whether trailing team has possession)
    - team records (eventually weight games within division higher)

- Produce and sort list with every response
    - Test execution time of algorithm so far (less than 1 minute essential)
    - Keep track of last update time and don't run algorithm if unchanged
    - Pull from local data every minute, run algorithm, pretty print results
    ^ Optimize as necessary (potentially use a database instead of local objects)

*** Thursday 10/26 at 11:55 PM

- Get working as web app with local data
    - Make server get next result from local file every minute and run parseAndSort
    ^ Find way to send output from parseAndSort to frontend to display
    - Make frontend look nice

*** Saturday 10/29 at 11:55 PM

- Get web app working on real time data
    ^ Write startup and exit functions to cleanly begin and end polling
    - Poll from NFL Scoreboard feed every minute and run parseAndSort
    ^ Where possible, optimize algorithm to only update objects when necessary

*** Sunday 10/30 at 11:55 PM

- *Optional* Use Materialize to improve look and feel

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

*** Saturday 11/05 at 11:55 PM

- Testing and adjusting
    - Use app throughout NFL Sunday
    - Address problems as necessary

*** Sunday 11/06 at 11:55 PM

***Note***
    - Minimum Viable Product acheived at this point
    - Everything after is gravy
    - Sanding rough edges most important, then fine tuning to look more impressive

- General bug fixing - Week of 11/07
    - Fix any remaining persistent bugs
    - Improve aspects that feel shoddy, but may not necessarily be bugs

- *Optional* Fine tuning: 11/14 - 11/30
    - Continue to tune default weighting
    ^ Continue to tune feedback mechanism
    - Improve UI

- Prepare deliverables: 12/01 - 12/08
"""


# TODO Prompt for username and password at startup
USERNAME = "devinjohnston17"
PASSWORD = "Iamthe71"

CURRENT_SEASON = "2016-2017-regular"

def getFullSchedule():
    url_schedule = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + \
            "/full_game_schedule.json"
    r = requests.get(url_schedule, auth=(USERNAME, PASSWORD))
    return r.text

def getScoreboard(fordate):
    url_scoreboard = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + \
            "/scoreboard.json?fordate=" + fordate
    r = requests.get(url_scoreboard, auth=(USERNAME, PASSWORD))
    return r.text

def getPlayByPlay(gameID):
    url_scoreboard = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + \
            "/game_playbyplay.json?gameid=" + gameID
    r = requests.get(url_scoreboard, auth=(USERNAME, PASSWORD))
    return r.text

# TODO
def parseJSON(requestText):
    decoded = json.loads(requestText)
    print decoded

# TODO Catch Ctrl-c
# TODO Encapsulate responses in json object (?)
def logResponses():
    log = open("log.txt", "w")
    fordate = "20161023"
    while (True):
        log.write(getScoreboard(fordate))
        log.write("\n\n")
        time.sleep(5)
    log.close()

def main():
    logResponses()

if __name__ == "__main__":
    main()
