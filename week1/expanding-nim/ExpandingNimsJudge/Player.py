class Player:
    
    def __init__(self):
        self.isUsedReset = False
        self.timeConsumed = 0
    
    def getIsUsedReset(self):
    	return self.isUsedReset
    
    def getTimeConsumed(self):
    	return self.timeConsumed
    
    def updateTimeConsumed(self, delta):
    	self.timeConsumed += delta

    def setIsUsedReset(self, isUsedReset):
    	self.isUsedReset = isUsedReset
