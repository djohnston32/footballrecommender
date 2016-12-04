import json

teamRankings = {'MIN': '17', 'MIA': '7', 'CAR': '25', 'ATL': '10', 'DET': '9', 'CIN': '27', 'NYJ': '28', 'DEN': '8', 'BAL': '14', 'NYG': '4', 'TEN': '18', 'NO': '23', 'DAL': '1', 'NE': '2', 'SEA': '6', 'CHI': '29', 'TB': '16', 'PIT': '13', 'JAX': '30', 'OAK': '3', 'HO': '15', 'GB': '22', 'WAS': '11', 'KC': '5', 'PHI': '21', 'BUF': '12', 'LA': '26', 'CLE': '32', 'IND': '19', 'ARI': '24', 'SF': '31', 'SD': '20'}

class Game:
    """
    Contains a real-time representation of a single football game
    """

    """
    gamestate = sbd["scoreboard"]["gameScore"][0]
    down = gamestate["currentDown"]
    distance = gamestate["currentYardsRemaining"]
    yardline = gamestate["lineOfScrimmage"] # dict
    """

    def __init__(self, gameDict, weights=(10,10,5,5)):
        self.homeTeam = gameDict["game"]["homeTeam"]["Abbreviation"]
        self.awayTeam = gameDict["game"]["awayTeam"]["Abbreviation"]

        # TODO Check for "currentQuarter" key
        self.isPrestart = "currentQuarter" not in gameDict
        if not self.isPrestart:
            self.quarter = int(gameDict["currentQuarter"])
            self.timeRemaining = int(gameDict["currentQuarterSecondsRemaining"])

            self.isHalftime = self.quarter == 2 and self.timeRemaining == 0

        self.homeScore = int(gameDict["homeScore"])
        self.awayScore = int(gameDict["awayScore"])

        if not (self.isPrestart or self.isHalftime):
            self.down = int(gameDict["currentDown"])
            self.toGo = int(gameDict["currentYardsRemaining"])
            if "teamInPossession" in gameDict:
                self.possession = gameDict["teamInPossession"]
                # dict of form: {"yardLine" : 35, "team" : "KC"}
                self.yardLine = gameDict["lineOfScrimmage"]
                self.yardLine["yardLine"] = int(self.yardLine["yardLine"])
            else:
                self.possession = ""

        self.rankscore = "None"
        self.pScore = 0
        self.pTime = 0
        self.pYardLine = 0
        self.pRank = 0
        self.priority = self.getPriority(weights)

    """
    TODO

    Time
        Make buckets smaller the later it is in the game
        Account for OT (quarter = 5)
    Score
        Change scale
        Make one- or two-score games a big p jump
    Yardline

    Team Records
        Get team record in Game object

    """
    # Weights is a tuple where values 0 through 3 are weights for score, time remaining,
    #    yardline, and team ranking, respectively
    def getPriority(self, weights):
        priority = 0
        if not (self.isPrestart or self.isHalftime):
            # Score
            scoreDiff = abs(self.homeScore - self.awayScore)
            pScore = 20 - scoreDiff
            pScore = 0 if pScore < 0 else pScore

            # Time Remaining
            pTime = (900 * (self.quarter - 1) + (900 - self.timeRemaining)) / 180

            #Yard Line
            if self.possession and self.possession != self.yardLine["team"]:
                pYardLine = 4 * (((50 - self.yardLine["yardLine"]) / 10) + 1)
            else:
                pYardLine = 0

            #Team Ranking (based on record)
            avgRank = (int(teamRankings[self.homeTeam]) + int(teamRankings[self.awayTeam])) / 2
            pRank = 2 * int(((32 - avgRank) / 32.0 * 10) + 1)


            self.pScore = pScore * weights[0]
            self.pTime = pTime * weights[1]
            self.pYardLine = pYardLine * weights[2]
            self.pRank = pRank * weights[3]

            self.rankscore = "pScore: " + str(self.pScore) + ", pTime: " + str(self.pTime) + \
                    ", pYardLine: " + str(self.pYardLine) + ", pRank: " + str(self.pRank)

            priority += self.pTime + self.pScore + self.pYardLine + self.pRank

        return priority

    def toJsonString(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        s = ""
        s += "Ranking Score: " + str(self.priority) + "\n"
        s += self.rankscore + "\n"
        s += self.homeTeam + ": " + str(self.homeScore) + "\n"
        s += self.awayTeam + ": " + str(self.awayScore) + "\n"
        if self.isPrestart:
            s += "Starting Soon..."
        elif self.isHalftime:
            s += "Halftime"
        else:
            s += "Quarter: " + str(self.quarter) + "   Remaining: " + \
                    str(self.timeRemaining / 60) + ":" + str(self.timeRemaining % 60).zfill(2) + "\n"
            if self.possession:
                s += "Possession: " + self.possession + "\n"
                s += str(self.down) + " and " + str(self.toGo) + " on the " + self.yardLine["team"] + \
                        " " + str(self.yardLine["yardLine"])
            else:
                s += "No Possession?"
        return s
