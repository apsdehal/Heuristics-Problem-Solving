import numpy as np
import utils
class Matchmaker:
    def __init__(self, numAttr):
        self.numAttr = numAttr
        self.initialData = []

    def parseInitialData(self, data):
        self.initialData = data
        # Parse logic here

    def guess(self, score):
        candidates = np.random.random(self.numAttr)
        return candidates
