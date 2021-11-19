

# TempBlock is a small class that keeps track of a single point of data.
# It tracks the time, temperature, and classification of the point of data.
# Classification refers to whether a block is the start, peak, or end of a shower.

class TempBlock:
    def __init__(self, xtemp, xtime, xclassification):
        self.myTemp = xtemp
        self.myTime = xtime
        self.myClassification = xclassification

    def temp(self):
        return self.myTemp

    def time(self):
        return self.myTime

    def classification(self):
        return self.myClassification

    def setClassification(self, newClassification):
        self.myClassification = newClassification