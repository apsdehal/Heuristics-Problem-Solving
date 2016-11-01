import util
import heapq
import copy

class Spoiler:
    def __init__(self, io):
        self.nStars = io.nStars
        self.reds = io.red
        self.blues = io.blue
        self.board = io.board
        self.boardSize = io.boardSize

    def move(self):
        self.stars = []
        count = 0
        blueCentroid = util.centroid(self.blues)
        redCentroid = util.centroid(self.reds)

        bpq = []

        for i in range(0, len(self.blues)):
            heapq.heappush(bpq, (self.getDist(self.blues[i], blueCentroid), i))

        rpq = []

        for i in range(0, len(self.reds)):
            heapq.heappush(rpq, (self.getDist(self.reds[i], redCentroid), i))

        while count != self.nStars:

            copyBpq = copy.deepcopy(bpq)

            while len(copyBpq) != 0 and count != self.nStars:
                currBlue = heapq.heappop(copyBpq)
                currBlue = self.blues[currBlue[1]]
                star = []
                if abs(blueCentroid[0] - currBlue[0]) > abs(blueCentroid[1] - currBlue[1]):
                    if blueCentroid[0] > currBlue[0]:
                        self.makeCorrectStar(currBlue, star, 'x', -1)
                    else:
                        self.makeCorrectStar(currBlue, star, 'x', 1)
                else:
                    if blueCentroid[1] > currBlue[1]:
                        self.makeCorrectStar(currBlue, star, 'y', -1)
                    else:
                        self.makeCorrectStar(currBlue, star, 'y', 1)

                if len(star) == 2:
                    print "Selecting", star
                    self.stars.append(star)
                count += 1

            if count == self.nStars:
                return self.formatOutput(self.stars)

            # We still have more self.stars to place, we will place near to reds
            copyRpq = copy.deepcopy(rpq)

            while len(copyRpq) != 0 and count != self.nStars:
                currRed = heapq.heappop(copyRpq)
                currRed = self.reds[currRed[1]]
                star = []
                if abs(redCentroid[0] - currRed[0]) > abs(redCentroid[1] - currRed[1]):
                    if redCentroid[0] > currRed[0]:
                        self.makeCorrectStar(currRed, star, 'x', -1)
                    else:
                        self.makeCorrectStar(currRed, star, 'x', 1)
                else:
                    if redCentroid[1] > currRed[1]:
                        self.makeCorrectStar(currRed, star, 'y', -1)
                    else:
                        self.makeCorrectStar(currRed, star, 'y', 1)

                if len(star) == 2:
                    print "Selecting", star
                    self.stars.append(star)
                count += 1

            if count == self.nStars:
                return self.formatOutput(self.stars)

    def makeCorrectStar(self, curr, star, direction, step):
        if direction == 'x':
            if curr[0] + step < 0 or curr[0] + step >= self.boardSize:
                # Reverse step if we have reach board end
                # It indirectly means guy can't come from this direction
                step = -1 * step
            star.append(curr[0] + step)
            star.append(curr[1])
        else:
            print "in make correct", curr, direction, step
            if curr[1] + step < 0 or curr[1] + step >= self.boardSize:
                step = -1 * step
            star.append(curr[0])
            star.append(curr[1] + step)

        self.makeStarValid(star, direction, step)

    def getDist(self, c1, c2):
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

    def formatOutput(self, stars):
        output = ""
        for star in stars:
            output += str(star[0]) + " " + str(star[1]) + " "

        print output
        return output.strip()

    def makeStarValid(self, star, direction, step):
        count = 0
        lastDirection = None
        while self.board[star[0]][star[1]] != '.' or not self.isValid(star):
            if count >= 5 * self.boardSize:
                if lastDirection == direction:
                    if lastDirection == 'diagonal':
                        self.getAValidStar(star)
                        return
                    direction = 'diagonal'
                else:
                    direction = 'y' if direction == 'x' else 'x'
                lastDirection = direction
                count = 0
            if direction == 'x':
                if star[0] + step < 0 or star[0] + step >= self.boardSize:
                    step = -1 * step;
                star[0] += step
                count += 1
            elif direction == 'y':
                if star[1] + step < 0 or star[1] + step >= self.boardSize:
                    step = -1 * step
                star[1] += step
                count += 1
            else:
                # We should not be here technically, but if we are it simply means
                # board is so full that we aren't able to place star
                stepX = step
                stepY = step
                if star[1] + stepY < 0 or star[1] + stepY >= self.boardSize:
                    stepY = -1 * stepY

                if star[0] + stepX < 0 or star[0] + stepX >= self.boardSize:
                    stepX = -1 * stepX

                star[0] += stepX
                star[1] += stepY
                count += 1

    def isValid(self, star):
        for s in self.stars:
            if self.getDist(s, star) < 4:
                return False

        return True

    def getAValidStar(self, star):
        flag = 0
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                star[0] = i
                star[1] = j
                if self.board[i][j] == '.' and self.isValid(star):
                    flag = 1
                    break
            if flag == 1:
                break

        if flag == 0:
            star.pop()
            star.pop()
