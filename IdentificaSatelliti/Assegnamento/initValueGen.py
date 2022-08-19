import math


class InitValueGen():
    def __init__(self, startValue: float):
        self.currentVal = startValue
        self.oldVal = None
        self.lowerBound = 0

    def genInitVal(self, value: float):
        if value <= self.currentVal + 50 and value >= self.currentVal - 50:
            raise Exception("init_value uguale a value")
        elif value > self.currentVal:
            self.lowerBound = self.currentVal
            temp = 0
            if self.oldVal:
                temp = abs(self.currentVal - self.oldVal) / 2
            else:
                temp = abs(self.currentVal) / 2
            self.oldVal = self.currentVal
            self.currentVal += temp
        elif value < self.currentVal:
            temp = 0
            if self.oldVal:
                temp = abs(self.currentVal - self.oldVal) / 2
            else:
                temp = abs(self.currentVal) / 2
            self.oldVal = self.currentVal
            self.currentVal -= temp

    def getBound(self):
        return self.lowerBound

    def testUpperLower(self):
        temp = 0
        if self.oldVal:
            temp = abs(self.currentVal - self.oldVal) / 2
        else:
            temp = abs(self.currentVal) / 2
        return(self.currentVal + temp, self.currentVal - temp)

    def getRange(self):
        if self.oldVal:
            return abs(self.currentVal - self.oldVal)
        return self.currentVal
