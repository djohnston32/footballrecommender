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

        self.quarter = int(gameDict["currentQuarter"])
        self.timeRemaining = int(gameDict["currentQuarterSecondsRemaining"])

        self.isHalftime = self.quarter == 2 and self.timeRemaining == 0

        self.homeScore = int(gameDict["homeScore"])
        self.awayScore = int(gameDict["awayScore"])

        if not self.isHalftime:
            self.possession = gameDict["teamInPossession"]
            self.down = int(gameDict["currentDown"])
            self.toGo = int(gameDict["currentYardsRemaining"])
            self.yardLine = gameDict["lineOfScrimmage"] # dict of form: {"yardLine" : 35, "team" : "KC"}
            self.yardLine["yardLine"] = int(self.yardLine["yardLine"])

        self.priority = self.getPriority()

    """
    TODO

    Time
        Make buckets smaller the later it is in the game

    """
    def getPriority(self):
        priority = 0
        if not self.isHalftime:
            # Time Remaining
            priority += (900 * (self.quarter - 1) + self.timeRemaining) / 180
        return priority

    def __str__(self):
        s = self.homeTeam + ": " + str(self.homeScore) + "\n"
        s += self.awayTeam + ": " + str(self.awayScore) + "\n"
        if self.isHalftime:
            s += "Halftime"
        else:
            s += "Quarter: " + str(self.quarter) + "   Remaining: " + str(self.timeRemaining) + "\n"
            s += "Possession: " + self.possession + "\n"
            s += str(self.down) + " and " + str(self.toGo) + " on the " + self.yardLine["team"] + " " + \
                str(self.yardLine["yardLine"])
        return s
