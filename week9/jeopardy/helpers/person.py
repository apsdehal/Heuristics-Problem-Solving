import utils
class Person:
    def __init__(self, numAttr):
        self.numAttr = numAttr
        self.initialWeights = []

    def getValidWeights(self):
        # Set initial weight here
        while(True):
            self.initialWeights = utils.get_valid_weights(self.numAttr)
            if(utils.checkSum(self.initialWeights)):
                return self.initialWeights
        return self.initialWeights 
        
    def getIdealCandidate(self):
        # Initial setup for ideal candidate, change accordingly
        return self.initialWeights > 0

    def getAntiIdealCandidate(self):
        # Initial setup for anti ideal candidate, change accordingly
        return self.initialWeights <= 0

    def getNewWeights(self, guess):
        # Use guess and self.initialWeights to calculate new data
        # send back initial weight for now
        response = utils.parseResponse(guess)
        noise = utils.getNoise(self.initialWeights,response)
        self.initialWeights = self.initialWeights + noise
        return self.initialWeights
