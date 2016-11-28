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

    def __init__(self, gameDict):
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
        self.priority = self.getPriority()

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
    def getPriority(self):
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
                pYardLine = 2 * ((50 - self.yardLine["yardLine"]) / 10)
            else:
                pYardLine = 0

            self.rankscore = "pTime: " + str(pTime) + ", pScore: " + str(pScore) + ", pYardLine: " + str(pYardLine)

            priority += pTime + pScore + pYardLine

        return priority

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
