import requests
from requests.auth import HTTPBasicAuth
import json
import time

# TODO Prompt for username and password at startup
USERNAME = "devinjohnston17"
PASSWORD = "Iamthe71"

CURRENT_SEASON = "2016-2017-regular"

def getFullSchedule():
    url_schedule = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + "/full_game_schedule.json"
    r = requests.get(url_schedule, auth=(USERNAME, PASSWORD))
    return r.text

def getScoreboard(fordate):
    url_scoreboard = "https://www.mysportsfeeds.com/api/feed/pull/nfl/" + CURRENT_SEASON + "/scoreboard.json?fordate=" + fordate
    r = requests.get(url_scoreboard, auth=(USERNAME, PASSWORD))
    return r.text

# TODO Catch Ctrl-c
# TODO Encapsulate responses in json object
def logResponses():
    log = open("log.txt", "w")
    fordate = "20161020"
    while (True):
        log.write(getScoreboard(fordate))
        log.write("\n")
        time.sleep(5)
    log.close()

def main():
    logResponses()

if __name__ == "__main__":
    main()
