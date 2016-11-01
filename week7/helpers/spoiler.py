import utils
import heapq
import copy

class Spoiler:
    def __init__(self, io):
        self.nStars = io.nStars
        self.reds = io.red
        self.blues = io.blue

    def move(self):
        stars = []
        count = 0
        blueCentroid = utils.centroid(self.blues)
        redCentroid = utils.centroid(self.reds)

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
                        star.push(currBlue[0] - 1)
                        star.push(currBlue[1])
                        self.makeStarValid(star, 'x', -1)
                    else:
                        star.push(currBlue[0] + 1)
                        star.push(currBlue[1])
                        self.makeStarValid(star, 'x', 1)
                else:
                    if blueCentroid[1] > currBlue[1]:
                        star.push(currBlue[0])
                        star.push(currBlue[1] - 1)
                        self.makeStarValid(star, 'y', -1)
                    else:
                        star.push(currBlue[0])
                        star.push(currBlue[1] + 1)
                        self.makeStarValid(star, 'y', 1)

                stars.append(star)
                count += 1

            if count == self.nStars:
                return self.formatOutput(stars)

            # We still have more stars to place, we will place near to reds
            copyRpq = copy.deepcopy(rpq)

            while len(copyRpq) != 0 and count != self.nStars:
                currRed = heapq.heappop(copyRpq)
                currRed = self.reds[currRed[1]]
                star = []
                if abs(redCentroid[0] - currRed[0]) > abs(redCentroid[1] - currRed[1]):
                    if redCentroid[0] > currRed[0]:
                        star.push(currRed[0] - 1)
                        star.push(currRed[1])
                        self.makeStarValid(star, 'x', -1)
                    else:
                        star.push(currRed[0] + 1)
                        star.push(currRed[1])
                        self.makeStarValid(star, 'x', 1)
                else:
                    if redCentroid[1] > currRed[1]:
                        star.push(currRed[0])
                        star.push(currRed[1] - 1)
                        self.makeStarValid(star, 'y', -1)
                    else:
                        star.push(currRed[0])
                        star.push(currRed[1] + 1)
                        self.makeStarValid(star, 'y', 1)

                stars.append(star)
                count += 1

            if count == self.nStars:
                return self.formatOutput(stars)


    def getDist(self, c1, c2):
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

    def formatOutput(self, stars):
        output = ""
        for star in stars:
            output += star[0] + " " + star[1] + " "

        return output.strip()
