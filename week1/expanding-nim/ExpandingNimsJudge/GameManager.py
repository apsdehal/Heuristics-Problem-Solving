import Server
import Player
import time
import copy
from enum import Enum

##Install Enum34 (pip install Enum34)
class ExitCodes(Enum):
    InvalidMove = 1
    InvalidResetBit = 2
    TLE = 3
    LegalWin = 4
    NotAvailable = 5

class GameManager():

    def __init__(self, initialStones):
        self.player = [Player.Player(), Player.Player()]
        self.server = Server.Server('', 50008)
        self.InitialStones = initialStones
        self.stonesLeft = self.InitialStones
        self.currentMax = min(2, self.InitialStones)
        self.turn = False #0 in bool, we will have player 0 and player 1
        self.TimeLimit = 120 #inseconds
        self.winner = None
        self.exitCode = ExitCodes.NotAvailable

    def shouldEndGame(self, stonesToDraw, resetBit, previousResetBit):
        if not self.isValidMove(stonesToDraw, previousResetBit):
            self.winner = int(not self.turn)
            self.exitCode = ExitCodes.InvalidMove
            return True
        if not self.isValidReset(resetBit):
            self.winner = int(not self.turn)
            self.exitCode = ExitCodes.InvalidResetBit
            return True
        if not self.isNotTLE():
            self.winner = int(not self.turn)
            self.exitCode = ExitCodes.TLE
            return True
        if self.stonesLeft == 0:
            self.winner = int(self.turn)
            self.exitCode = ExitCodes.LegalWin
            return True
        return False

    def isNotTLE(self):
        curPlayer = self.player[int(self.turn)]
        # if curPlayer.getTimeConsumed() > self.TimeLimit:
        #     return False
        return True

    def isValidReset(self, resetBit):
        curPlayer = self.player[int(self.turn)]
        if (resetBit and curPlayer.getIsUsedReset()):
            return False
        return True

    def parseResponse(self, playerResponse):
        if len(playerResponse.split(' ')) != 2:
            return False
        playerResponse = playerResponse.split(' ')
        try:
            playerResponse = [int(playerResponse[i]) for i in [0, 1]]
        except ValueError:
            return False
        return playerResponse

    def isValidMove(self, stonesToDraw, previousResetBit):
        if (stonesToDraw > self.stonesLeft or stonesToDraw > self.currentMax + 1
            or (previousResetBit and stonesToDraw > 3) or stonesToDraw <= 0):
            return False
        return True

    def updateMove(self, stonesToDraw, resetBit):
        self.stonesLeft-= stonesToDraw
        self.currentMax = max(stonesToDraw, self.currentMax)
        if resetBit:
            self.player[int(self.turn)].setIsUsedReset(True)
        if self.stonesLeft == 0:
            self.winner = self.turn
            self.exitCode = ExitCodes.LegalWin
        self.turn = not self.turn

    def statusUpdate(self):
        curPlayer = self.player[int(self.turn)]
        print "Stones Left: ", self.stonesLeft
        print "Turn: Player ", int(self.turn)
        print "Reset status: ", curPlayer.getIsUsedReset()
        print "Time consumed: ", curPlayer.getTimeConsumed()

    def run(self):
        self.server.establishConnection()
        stonesToDraw = 0
        resetBit = False
        isGameOver = False
        curGameConfig = ''
        playerResponse = ''
        while 1:
            curPlayer = self.player[int(self.turn)]
            self.statusUpdate()
            curGameConfig = "{} {} {} {}".format(self.stonesLeft,
                self.currentMax, int(resetBit), int(isGameOver))
            self.server.send(curGameConfig, int(self.turn))
            start = time.time()
            playerResponse = self.server.receive(int(self.turn))
            print playerResponse
            timeTaken = time.time() - start
            curPlayer.updateTimeConsumed(timeTaken)
            playerResponse = self.parseResponse(playerResponse)
            previousResetBit = resetBit
            if playerResponse == False:
                self.shouldEndGame(0, 0, 0)
                break
            resetBit = bool(playerResponse[1])
            if self.shouldEndGame(playerResponse[0], resetBit, previousResetBit):
                break
            self.updateMove(playerResponse[0], resetBit)
            if self.winner != None:
                break

        self.server.send('0 0 0 1', 0)
        self.server.send('0 0 0 1', 1)

        print "WINNER  : Player ", int(self.winner)
        print "exitCode: ", self.exitCode.name


def main():
    num = input()
    print num
    gm = GameManager(num)
    gm.run()
    print "In GameManager"
if __name__ == '__main__':
    main()
