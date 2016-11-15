import numpy as np
import utils
import copy
import random

class Matchmaker:
    def __init__(self, numAttr, lam = 0.005):
        self.numAttr = numAttr
        self.initialCandidates = []
        self.lam = lam
        self.usedMiniIndex = []
        random.seed(None)

    def parseInitialData(self, data):
        self.candidates = copy.deepcopy(data)
        self.estimate = np.zeros(self.numAttr)
        self.train()

    def train(self):

        # Add more training data in which score is 0, so we know which side is bad
        for x in np.arange(-1.00, 1.05, 0.05):
            candidate = np.ones(self.numAttr) * x
            score = 0.0
            self.candidates.append((candidate, score))


        self.A = np.array([candidate[0] for candidate in self.candidates])

        # convert score also in 2d array, so we have same shape
        self.B = np.array([np.array(candidate[1]) for candidate in self.candidates])

        # Regularization matrix
        self.R = np.identity(self.A.shape[1]) * self.lam

        # Apply Tikhonov/Ridge Regression
        # Dot of transpose
        sub = np.dot(self.A.T, self.A) + np.dot(self.R.T, self.R)
        self.estimate = np.dot(np.linalg.inv(sub), np.dot(self.A.T, self.B)).reshape(self.numAttr)

        # self.truncateEstimate()

    def truncateEstimate(self):
        self.estimate = np.trunc(self.estimate * 100) / 100.0

    def guess(self, candidate, score, index):
        if index != 0:
            self.reEstimate(candidate, score)

        return self.findCandidate()

    def reEstimate(self, candidate, score):
        assert(len(candidate) == self.numAttr)

        self.candidates.append((candidate, score))

        self.A = np.vstack((self.A, np.array([candidate])))

        self.B = np.append(self.B, np.array(score))

        self.R = np.identity(self.A.shape[1]) * self.lam
        print self.A.shape, self.R.shape, self.B.shape

        sub = np.dot(self.A.T, self.A) + np.dot(self.R.T, self.R)
        self.estimate = np.dot(np.linalg.inv(sub), np.dot(self.A.T, self.B)).reshape(self.numAttr)

        # self.truncateEstimate()

    def findCandidate(self):
        while 1:
            cand = np.array(self.estimate > 0.0, dtype = float).reshape(self.numAttr)

            cand = cand % 1.0000001

            if self.checkUniqueness(cand) == False:
                cand = self.addNoise()

                if self.checkUniqueness(cand) == True:
                    return cand
            else:
                return cand

    def checkUniqueness(self, cand = []):
        for c in self.candidates:
            if ((c[0] == cand).all()):
                return False
        return True

    def addNoise(self):
        cWeights = self.estimate.copy()

        minis = utils.getAbsMinNegPos(cWeights, self.usedMiniIndex)

        cWeights[minis[0]] = -1 * cWeights[minis[0]]
        cWeights[minis[1]] = -1 * cWeights[minis[1]]

        self.usedMiniIndex.append(minis[0])
        self.usedMiniIndex.append(minis[1])

        # noise = np.random.normal(size = self.numAttr)
        # change = np.asarray(np.abs(noise) > 2.0, dtype = int)
        #
        # for i in range(len(change)):
        #     if change[i] > 0.0:
        #         if random.random() > 0.5:
        #             cWeights[i] += cWeights[i] * 0.2
        #         else:
        #             cWeights[i] -= cWeights[i] * 0.2

        cand = np.array(cWeights > 0, dtype = float).reshape(self.numAttr)

        cand = cand % 1.000001

        return cand
